from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.index, name='blog.index'),
    path('<int:page>/', views.index, name='blog.index'),
    path('article/<int:id>', views.show, name='blog.show'),
    path('article/<int:id>/edit', views.edit, name='blog.edit'),
    path('article/create', views.create, name='blog.create'),
]