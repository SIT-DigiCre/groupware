from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.index, name='blog.index'),
    path('<int:page>/', views.index, name='blog.index'),
    path('article/<int:id>', views.show, name='blog.show'),
    path('article/<int:id>/edit', views.edit, name='blog.edit'),
    path('article/create', views.create, name='blog.create'),
    path('tag/create',views.create_tag,name='blog.create_tag'),
    path('tag/<int:id>',views.show_tag,name='blog.show_tag'),
    path('tag/<int:id>/edit',views.edit_tag,name='blog.edit_tag'),
    path('tag',views.index_tag,name='blog.index_tag'),
    path('article/<int:id>/tags',views.edit_art_tags,name='blog.edit_art_tags'),
  
    path('relay_2020summer/', views.relay, name='blog.relay'),
    path('relay_2020summer/add_check/<int:year>/<int:month>/<int:day>', views.relay_add_check, name='blog.relay_add_check'),
    path('relay_2020summer/add/<int:year>/<int:month>/<int:day>', views.relay_add, name='blog.relay_add'),
    path('mypage',views.mypage,name='blog.mypage'),
]