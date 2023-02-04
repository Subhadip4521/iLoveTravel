from django.contrib import admin
from django.urls import path
from kolkata import views

urlpatterns = [
    path("postComment", views.postComment, name='postComment'),

    path("", views.kolkata, name='kolkata'),
    path("<str:slug>", views.blogpost, name='blogpost'),
    
    
]