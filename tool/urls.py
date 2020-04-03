from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='tool.index'),
    path('<int:id>', views.show, name='tool.show'),
    path('create', views.create,name='tool.create'),
]