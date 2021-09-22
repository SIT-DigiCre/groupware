from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.index, name='blog.index'),
    path('article/<int:id>', views.show, name='blog.show'),
    path('article/<int:id>/edit', views.edit, name='blog.edit'),
    path('article/create', views.create, name='blog.create'),
    path('tag/create', views.create_tag, name='blog.create_tag'),
    path('tag/<int:id>', views.show_tag, name='blog.show_tag'),
    path('tag/<int:id>/edit', views.edit_tag, name='blog.edit_tag'),
    path('tag', views.index_tag, name='blog.index_tag'),
    path(
        'article/<int:id>/tags',
        views.edit_art_tags,
        name='blog.edit_art_tags'),
    path(
        'article/<int:art_id>/tags/delete/<int:tag_id>',
        views.delete_art_tag,
        name='blog.delete_art_tag'),
    path(
        'event/<int:id>/',
        views.relay,
        name='blog.relay'),
    path('event/<int:id>/add_check/<int:year>/<int:month>/<int:day>',
         views.relay_add_check, name='blog.relay_add_check'),
    path('event/<int:id>/add/<int:year>/<int:month>/<int:day>',
         views.relay_add, name='blog.relay_add'),
    path('event/<int:id>/edit/<int:year>/<int:month>/<int:day>',
         views.relay_edit, name='blog.relay_edit'),
    path('event/<int:id>/delete/<int:year>/<int:month>/<int:day>',
         views.relay_delete, name='blog.relay_delete'),

    path('article/<int:id>/ogp_image', views.GenOGPImageAPIView.as_view(), name='blog.ogp_image'),
    # path('event/<event_name>/',views.event_index,name='blog.event_index'),
    path('mypage', views.mypage, name='blog.mypage'),
]
