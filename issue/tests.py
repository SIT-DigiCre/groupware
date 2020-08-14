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

        # TODO: 
        # extension in category is temporarily added in my environment.
        # please update this information along with set category.
        data = {
            "title": "test",
            "category": "test category",
            "content": "test content"
        }
        response = client.post('/issue/create', data)
        self.assertRedirects(response, '/issue/', status_code=302, target_status=200, msg_prefix='', fetch_redirect_response=True)
        
    def make_authenticated_user(self):
        """
        makes authenticated user for testing
        """

        user = User.objects.create_user(self.test_user["username"],self.test_user["email"], self.test_user["last_name"])
        user.first_name = self.test_user["first_name"]
        user.student_id = self.test_user["student_id"]
        user.is_active = True
        user.save()

        client = Client()
        client.force_login(user)
        return user, client
