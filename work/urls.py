from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='work.index'),
    path('<int:id>', views.show, name='work.show'),
    path('create', views.create,name='work.create'),
    path('edit/<int:id>', views.edit,name='work.edit'),
]