from django.conf.urls import include
from django.urls import path
from blog import views as blog_views
from strage import views as strage_views
from work import views as work_views
from rest_framework import routers

blog_router = routers.DefaultRouter()
blog_router.register('article', blog_views.ArticleViewSet)
blog_router.register('my_article', blog_views.MyArticlesViewSet)
blog_router.register('article_tag', blog_views.ArticleTagViewSet)

strage_router = routers.DefaultRouter()
strage_router.register('fileobject', strage_views.FileObjectViewSet)

work_router = routers.DefaultRouter()
work_router.register('item', work_views.WorkItemViewSet)
work_router.register('tag', work_views.WorkTagViewSet)

urlpatterns = [
    path('blog/', include(blog_router.urls)),
    path('strage/', include(strage_router.urls)),
    path('strage/fileobject/upload', strage_views.UploadFileObjectView.as_view()),
    path('work/', include(work_router.urls)),
]
