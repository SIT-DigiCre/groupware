from django.test import TestCase, RequestFactory, Client
from account.models import User
from django.contrib.auth import get_user_model

class IssuePageTest(TestCase):

    test_user = {
        "username": "test",
        "email": "al17000@shibaura-it.ac.jp",
        "last_name": "fuga",
        "first_name": "hoge",
        "student_id": "al17000",
        "is_active": True,
    }
    
    def test_issue_page_walk_status_ok(self):
        """
        tests that it returns 200 OK status
        while walking under /issue pages.
        """

        # make authenticated user
        user, client = self.make_authenticated_user()
        self.assertTrue(user.is_active, True)

        # access  /issue/ for checking status
        response = client.get('/issue/')
        self.assertEqual(response.status_code, 200)

        # access /issue/create for checking status
        response = client.get('/issue/create')
        self.assertEqual(response.status_code, 200)
        
    def test_create_issue_page_status_ok(self):
        """
        tests that it can create issue
        and it will have been registered.
        """
        # make authenticated user
        user, client = self.make_authenticated_user()
        self.assertTrue(user.is_active, True)

        # access /issue/create for checking status
        response = client.get('/issue/create')
        self.assertEqual(response.status_code, 200)        

        # send post request
        data = {
            "title": "test data",
            "category": "1", # number is set by fixture
            "content": "test content"
        }
        response = client.post('/issue/create', data)

        # check redirects
        self.assertRedirects(response, '/issue/', status_code=302,
                             target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)
        
        # check if it's registered
        response = client.get('/issue/')
        self.assertIn(data["title"], response.content.decode())
        self.assertIn(data["category"], response.content.decode())
        self.assertIn(data["content"], response.content.decode())

    def test_create_issue_with_invalid_data(self):
        """
        tests that it can create issue
        and it will have been registered.
        """
        # make authenticated user
        user, client = self.make_authenticated_user()
        self.assertTrue(user.is_active, True)

        # send post request
        data = {
            "title": "test data",
            "category": "-1", # invalid
            "content": "test content"
        }
        response = client.post('/issue/create', data)

        # check redirects
        self.assertRedirects(response, '/issue/', status_code=302,
                             target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)
        
        # check if it's registered
        response = client.get('/issue/')
        self.assertNotIn(data["title"], response.content.decode())
        self.assertNotIn(data["content"], response.content.decode())

    def test_edit_issue(self):
        # make authenticated superuser
        user, client = self.make_authenticated_superuser()
        self.assertTrue(user.is_active, True)

        # send post request
        data = {
            "title": "test data",
            "category": "1", # number is set by fixture
            "content": "test content"
        }
        response = client.post('/issue/create', data)
        response = client.get('/issue/')

        # check if exists delete link
        self.assertContains(response, 'href="{0}"'.format('/issue/edit/1'))

        response = client.get('/issue/edit/1')

        # send post request
        data = {
            "status": "2", # 進行中
            "assignee": "1", # 自分
            "content": "updated test content"
        }
        self.assertContains(response, 'action="{0}"'.format('/issue/edit/1'))
        response = client.post('/issue/edit/1', data)
        
        self.assertRedirects(response, '/issue/', status_code=302,
                             target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)

        
    def test_delete_issue(self):
        # make authenticated superuser
        user, client = self.make_authenticated_superuser()
        self.assertTrue(user.is_active, True)

        # send post request
        data = {
            "title": "test data",
            "category": "1", # number is set by fixture
            "content": "test content"
        }
        response = client.post('/issue/create', data)
        response = client.get('/issue/')

        # check if exists delete link
        self.assertContains(response, 'href="{0}"'.format('/issue/delete/1'))

        response = client.get('/issue/delete/1')
        self.assertContains(response, 'action="{0}"'.format('/issue/delete/1'))
        response = client.post('/issue/delete/1')
        
        self.assertRedirects(response, '/issue/', status_code=302,
                             target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)
    
        
    def make_authenticated_user(self):
        """
        makes authenticated user for testing
        """

        user = User.objects.create_user(self.test_user["username"],
                                        self.test_user["email"],
                                        self.test_user["last_name"])
        user.first_name = self.test_user["first_name"]
        user.student_id = self.test_user["student_id"]
        user.is_active = True
        user.save()

        client = Client()
        client.force_login(user)
        return user, client

    
    def make_authenticated_superuser(self):
        """
        makes authenticated user for testing
        """

        user = User.objects.create_user(self.test_user["username"],
                                        self.test_user["email"],
                                        self.test_user["last_name"])
        user.first_name = self.test_user["first_name"]
        user.student_id = self.test_user["student_id"]
        user.is_active = True
        user.is_superuser = True
        user.save()

        client = Client()
        client.force_login(user)
        return user, client
