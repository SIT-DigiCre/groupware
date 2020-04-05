from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='member.index'),
    path('<int:id>', views.show, name='member.show'),
    path('edit', views.edit, name='member.edit'),
]