from django.urls import path
from django.views.generic import TemplateView
from main.views import LoginView, LogoutView, RegisterView, DashboardView

urlpatterns = [
    path('', TemplateView.as_view(template_name = 'main/index.html'), name = 'index'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('register/', RegisterView.as_view(), name = 'register'),
    path('dashboard/', DashboardView.as_view(), name = 'dashboard'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
]