from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create', views.create, name='create'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout')
]