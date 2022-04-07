from django.shortcuts import redirect, render
from django.http import HttpResponseBadRequest
from django.views import View
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags import humanize
from django.utils import timezone
from django.db.models import Avg
from django.conf import settings
from main.forms import LoginForm, RegisterForm
from api.models import Visitor
from api.urls import endpoints
from api.utils import getData
from main.utils import get_total_days_of_month
from io import BytesIO
from main import signal
from main.models import Token
import matplotlib.pyplot as plt
import base64, requests

plt.rcParams["font.family"] = "monospace"


class IndexView(View):
    def get(self, request: WSGIRequest):
        total_requests = Visitor.objects.count()
        total_requests_success = Visitor.objects.filter(success__in = [True]).count()
        total_requests_failed = Visitor.objects.filter(success__in = [False]).count()

        if total_requests:
            avg_proccess_time = round(Visitor.objects.aggregate(Avg('proccess_time'))['proccess_time__avg'], 4)
            total_requests_endpoint = {}
            for endpoint in endpoints:
                total = Visitor.objects.filter(endpoint = endpoint).count()
                total_requests_endpoint[endpoint] = total
            
            total_requests_endpoint = sorted(total_requests_endpoint.items(), key = lambda x: x[1], reverse = True)
            total_requests_endpoint = dict([x for x in total_requests_endpoint if x[1] > 0][:4])
            total_requests_endpoint_int = sum(total_requests_endpoint.values())
            if (total_requests - total_requests_endpoint_int) > 0:
                total_requests_endpoint['other'] = total_requests - total_requests_endpoint_int

            fig = plt.figure()
            ax = fig.add_axes([0,0,1,1])
            ax.pie(total_requests_endpoint.values(), labels = total_requests_endpoint.keys(), autopct = '%1.2f%%')

            most_popular_endpoints_image = BytesIO()
            fig.savefig(most_popular_endpoints_image, format = 'png')
            most_popular_endpoints_image.seek(0)

            most_popular_endpoints_b64image = base64.b64encode(most_popular_endpoints_image.getvalue()).decode()
            most_popular_endpoints_image_uri = f'data:image/png;base64,{most_popular_endpoints_b64image}'
        else:
            avg_proccess_time = 0
            most_popular_endpoints_image_uri = None

        context = {
            'avg_proccess_time': avg_proccess_time,
            'total_requests': total_requests,
            'total_requests_success': total_requests_success,
            'total_requests_failed': total_requests_failed,
            'most_popular_endpoints_image_uri': most_popular_endpoints_image_uri
        }
        return render(request, 'main/index.html', context)


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

        data = getData(request)
        c_response = data.get('g-recaptcha-response')

        result_check_capctha = requests.post('https://www.google.com/recaptcha/api/siteverify', data = {
            'secret': settings.G_CAPCTHA_SECRET_KEY,
            'response': c_response
        }).json()
        if not result_check_capctha.get('success'):
            context = {
                'error_msg': 'Captcha not valid!'
            }
            return render(request, 'main/login.html', context)

        
        user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
        if not user:
            context = {
                'error_msg': 'Wrong username / password!'
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

        data = getData(request)
        c_response = data.get('g-recaptcha-response')

        result_check_capctha = requests.post('https://www.google.com/recaptcha/api/siteverify', data = {
            'secret': settings.G_CAPCTHA_SECRET_KEY,
            'response': c_response
        }).json()
        if not result_check_capctha.get('success'):
            context = {
                'error_msg': 'Captcha not valid!'
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

        context = {
            'success_msg': 'Daftar berhasil! silahkan login'
        }

        return render(request, 'main/register.html', context)
        

@method_decorator(login_required, name = 'dispatch')
class DashboardView(View):
    def get(self, request: WSGIRequest):
        # total_requests = Visitor.objects.filter(user__id = request.user.id).count()
        visitors = Visitor.objects.filter(user__id = request.user.id).all()
        token_obj = Token.objects.get(user__id = request.user.id)
        token = token_obj.token
        total_requests = len(visitors)
        total_requests_today = 0
        total_requests_yesterday = 0
        now = timezone.now()
        month_year_now = now.strftime('%m%Y')
        total_days = get_total_days_of_month(now)
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


        # fig, ax = plt.subplots()
        # ax.plot(days, total_requests_per_day)
        # ax.set(xlabel='Date by Day', ylabel='Total Request', title = 'API Request')
        # image = BytesIO()
        # fig.savefig(image, format = 'png')
        # image.seek(0)
        # image_base64 = base64.b64encode(image.getvalue()).decode()
        # image_data = f'data:image/png;base64,{image_base64}'

        total_requests_success = Visitor.objects.filter(user__id = request.user.id, success__in = [True]).count()
        total_requests_failed = Visitor.objects.filter(user__id = request.user.id, success__in = [False]).count()

        if total_requests:
            avg_proccess_time = round(Visitor.objects.filter(user__id = request.user.id).aggregate(Avg('proccess_time'))['proccess_time__avg'], 4)
            total_requests_endpoint = {}
            for endpoint in endpoints:
                total = Visitor.objects.filter(user__id = request.user.id, endpoint = endpoint).count()
                total_requests_endpoint[endpoint] = total
        
            
            total_requests_endpoint = sorted(total_requests_endpoint.items(), key = lambda x: x[1], reverse = True)
            total_requests_endpoint = dict([x for x in total_requests_endpoint if x[1] > 0][:4])
            total_requests_endpoint_int = sum(total_requests_endpoint.values())
            if total_requests - total_requests_endpoint_int > 0:
                total_requests_endpoint['other'] = total_requests - total_requests_endpoint_int

            fig = plt.figure()
            ax = fig.add_axes([0,0,1,1])
            ax.pie(total_requests_endpoint.values(), labels = total_requests_endpoint.keys(), autopct = '%1.2f%%')

            most_popular_endpoints_image = BytesIO()
            fig.savefig(most_popular_endpoints_image, format = 'png')
            most_popular_endpoints_image.seek(0)

            most_popular_endpoints_b64image = base64.b64encode(most_popular_endpoints_image.getvalue()).decode()
            most_popular_endpoints_image_uri = f'data:image/png;base64,{most_popular_endpoints_b64image}'
        else:
            avg_proccess_time = 0
            most_popular_endpoints_image_uri = None

        context = {
            'token': token,
            'user': request.user,
            'total_requests': total_requests,
            'total_requests_today': total_requests_today,
            'total_requests_yesterday': total_requests_yesterday,
            'most_popular_endpoints_image_uri': most_popular_endpoints_image_uri,
            'avg_proccess_time': avg_proccess_time,
            'total_requests_success': total_requests_success,
            'total_requests_failed': total_requests_failed
        }
        return render(request, 'main/dashboard.html', context)


@method_decorator(login_required, name = 'dispatch')
class LogoutView(View):
    def get(self, request: WSGIRequest):
        logout(request)
        return redirect('login')