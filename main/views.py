from django.shortcuts import redirect, render
from django.http import HttpResponseBadRequest, request
from django.views import View
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from main.forms import LoginForm, RegisterForm
from main.models import Customer

class LoginView(View):
    def get(self, request: WSGIRequest):
        if request.user.is_authenticated:
            return redirect('dashboard')
    
        return render(request, 'main/login.html')

    def post(self, request: WSGIRequest):
        if request.user.is_authenticated:
            return redirect('dashboard')

        form = LoginForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest('Bad Request')
        
        user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
        if not user:
            context = {
                'error_msg': 'Username / password salah!'
            }
            return render(request, 'main/login.html', context)

        

class RegisterView(View):
    def get(self, request: WSGIRequest):
        if request.user.is_authenticated:
            return redirect('dashboard')

        return render(request, 'main/register.html')

    def post(self, request: WSGIRequest):
        if request.user.is_authenticated:
            return redirect('dashboard')
            
        form = RegisterForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest('Bad Request')
        
        if not form.cleaned_data['username'].isalnum():
            context = {
                'error_msg': 'Username hanya mendukung alphanumeric'
            }
            return render(request, 'main/register.html', context)

        if len(form.cleaned_data['password']) < 5 or len(form.cleaned_data['password']) > 20:
            context = {
                'error_msg': 'Password minimal 5 karakter, maksimal 20 karakter'
            }
            return render(request, 'main/register.html', context)

        if User.objects.filter(username = form.cleaned_data['username'].lower()).first():
            context = {
                'error_msg': 'Username sudah ada'
            }
            return render(request, 'main/register.html', context)
        
        if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
            context = {
                'error_msg': 'Password dan konfirmasi password tidak sama'
            }
            return render(request, 'main/register.html', context)
        
        
        user = User.objects.create_user(
            username = form.cleaned_data['username'].lower(),
            password = form.cleaned_data['password']
        )
        user.save()

        customer = Customer(
            user = user,
            api_key = get_random_string(),
        )
        customer.save()

        context = {
            'success_msg': 'Daftar berhasil! silahkan login'
        }

        return render(request, 'main/register.html', context)
        

@method_decorator(login_required, name = 'dispatch')
class DashboardView(View):
    def get(self, request: WSGIRequest):
        customer = Customer.objects.get(user__id = request.user.id)
        context = {
            'customer': customer
        }
        return render(request, 'main/dashboard.html', context)