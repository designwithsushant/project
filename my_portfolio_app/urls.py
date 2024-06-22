from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginpage, name="loginpage"),
    path('administrator/', views.adminpage, name="adminpage"),
    path('add-project/', views.add_project, name="add_project"),
    path('loginuser/', views.loginback, name="loginback"),
    path('logout/', views.logoutuser, name="logoutuser"),
    path('administrator/My-Projects/', views.projectspage, name="projectspage"),
]