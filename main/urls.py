from django.urls import path
from main.views import IndexView, LoginView, LogoutView, RegisterView, DashboardView

urlpatterns = [
    path('', IndexView.as_view(), name = 'index'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('register/', RegisterView.as_view(), name = 'register'),
    path('dashboard/', DashboardView.as_view(), name = 'dashboard'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
]