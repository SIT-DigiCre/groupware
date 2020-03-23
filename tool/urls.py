from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('show/<int:page>', views.show, name='show'),
    path('create', views.create, name='create'),
]