from django.shortcuts import redirect, render
from django.http import HttpResponseBadRequest
from django.views import View
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags import humanize
from django.utils.crypto import get_random_string
from django.utils import timezone
from main.forms import LoginForm, RegisterForm
from main.models import Customer, Visitor
from main.utils import get_total_days_of_month
from io import BytesIO
import matplotlib.pyplot as plt
import base64

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
        
        login(request, user)
        return redirect('dashboard')

        

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
        visitors = Visitor.objects.filter(customer__id = customer.id).all()
        total_requests = len(visitors)
        total_requests_today = 0
        total_requests_yesterday = 0
        now = timezone.now()
        month_year_now = now.strftime('%m%Y')
        total_days = get_total_days_of_month(now)
        print(total_days)
        days = [i + 1 for i in range(total_days)]
        total_requests_per_day = [0] * total_days

        for visitor in visitors:
            humanize_time = humanize.naturalday(visitor.date)
            day = int(visitor.date.strftime('%d'))

            if visitor.date.strftime('%m%Y') == month_year_now:
                total_requests_per_day[day - 1] += 1

            if humanize_time == 'today':
                total_requests_today += 1
            elif humanize_time == 'yesterday':
                total_requests_yesterday += 1


        fig, ax = plt.subplots()
        ax.plot(days, total_requests_per_day)
        ax.set(xlabel='Date by Day', ylabel='Total Request', title = 'API Request')
        image = BytesIO()
        fig.savefig(image, format = 'png')
        image.seek(0)
        image_base64 = base64.b64encode(image.getvalue()).decode()
        image_data = f'data:image/png;base64,{image_base64}'

        context = {
            'customer': customer,
            'total_requests': total_requests,
            'total_requests_today': total_requests_today,
            'total_requests_yesterday': total_requests_yesterday,
            'image': image_data,
        }
        return render(request, 'main/dashboard.html', context)


@method_decorator(login_required, name = 'dispatch')
class LogoutView(View):
    def get(self, request: WSGIRequest):
        logout(request)
        return redirect('login')