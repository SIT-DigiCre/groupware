from django.urls import path
from . import views

app_name = 'issue'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>', views.show, name='show'),
    path('create', views.create, name='create'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('edit/<int:id>', views.edit, name='edit'),
]