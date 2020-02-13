from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.jump, name='jump'),
    path('<channel_name>/', views.index, name='index'),
    path('<channel_name>/show/<int:id>', views.show, name='index'),
    path('<channel_name>/<int:page>', views.index, name='index'),
]