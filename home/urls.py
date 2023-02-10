from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='home'),
    path("signup/", views.signupUser, name='signup'),
    path("login", views.loginUser, name='login'),
    path("logout/", views.logoutUser ,name='logout'),
    
    path("about/", views.about, name='about'),
    path("contact/", views.contact, name='contact'),
    path("search/", views.search, name='search'),


    
    
]