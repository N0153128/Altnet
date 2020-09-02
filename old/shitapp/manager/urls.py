#from django.urls import path, include
#from . import views
#from django.contrib.auth import views as auth_views
#from django.views.generic.base import View
#from django.contrib.auth import login

#app_name = 'manager'
#urlpatterns = [
#    path('', views.index, name= 'index'),
#    path('auth/', views.authsh, name = 'auth'),
#    path('login/',  auth_views.LoginView.as_view(template_name = 'registration/login.html'), name='login'),
#    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
#    path('user/', views.account, name='user'),
#]