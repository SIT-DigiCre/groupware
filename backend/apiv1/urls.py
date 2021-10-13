from django.conf.urls import include
from django.urls import path
from blog import views as blog_views
from storage import views as strage_views
from work import views as work_views
from account import views as account_views
from rest_framework import routers

blog_router = routers.DefaultRouter()
blog_router.register('article', blog_views.ArticleViewSet)
blog_router.register('my_article', blog_views.MyArticlesViewSet)
blog_router.register('article_tag', blog_views.ArticleTagViewSet)

storage_router = routers.DefaultRouter()
storage_router.register('fileobject', strage_views.FileObjectViewSet)
storage_router.register('myfileobject', strage_views.MyFileObjectViewSet)

work_router = routers.DefaultRouter()
work_router.register('item', work_views.WorkItemViewSet)
work_router.register('tag', work_views.WorkTagViewSet)

account_router = routers.DefaultRouter()
account_router.register('userinfo', account_views.MyUserViewSet)

urlpatterns = [
    path('blog/', include(blog_router.urls)),
    path('storage/', include(storage_router.urls)),
    path('storage/fileobject/upload', strage_views.UploadFileObjectView.as_view()),
    path('work/', include(work_router.urls)),
    path('account/', include(account_router.urls)),
]
