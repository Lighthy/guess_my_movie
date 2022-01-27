from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('find', views.find, name='find'),
    path('find_movie', views.find_movie, name='find_movie'),
]