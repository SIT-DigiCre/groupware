from django.conf.urls import include
from django.urls import path
from blog import views as blog_views
from rest_framework import routers

blog_router = routers.DefaultRouter()
blog_router.register('articles', blog_views.ArticleViewSet)
blog_router.register('article_tag', blog_views.ArticleTagViewSet)

urlpatterns = [
    path('blog/', include(blog_router.urls)),
]
