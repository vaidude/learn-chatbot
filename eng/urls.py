"""
URL configuration for aitutor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name = 'index'),
    path('index/', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('register/', views.RegisterUser, name='register'),
    path('login/', views.LoginUser, name='login'),
    
    path('adlogin/', views.adlogin, name='adlogin'),
    path('adhome/', views.adhome, name='adhome'),
    path('chat/', views.chatbot, name='chat'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('process_voice/', views.process_voice, name='process_voice'),
    path('userlist/', views.userlist, name='userlist'),
    path('deleteuser/<int:id>', views.deleteuser, name='deleteuser'),
    path('feedback/', views.feedback_rate, name='feedback'),
    path('feedbacklist/', views.feedbacklist, name='feedbacklist'),
 
    

]
