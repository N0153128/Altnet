from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'Manager'
urlpatterns = [
    path('auth/', views.authsh.as_view(), name='auth'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('me/', views.meview, name='me'),
]