from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ringi.index'),
    path('<int:page>', views.index, name='ringi.index'),
    path('create', views.create, name='ringi.create'),
]