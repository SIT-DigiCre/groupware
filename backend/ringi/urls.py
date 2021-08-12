from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ringi.index'),
    path('create', views.create, name='ringi.create'),
    path('show/<int:id>', views.show, name='ringi.show'),
    path('edit/<int:id>', views.edit, name='ringi.edit'),
    path('delete/<int:id>', views.delete, name='ringi.delete'),
]