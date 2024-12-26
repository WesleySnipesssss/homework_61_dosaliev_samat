from django.urls import path
# from accounts.views import login_view, logout_view
from django.contrib.auth.views import LoginView, LogoutView
from .views import register_view

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
]
