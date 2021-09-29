from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
# from main.models import Customer
from api.utils import getData
import json

def api_key_required(func):
    def inner(request: WSGIRequest, *args, **kwargs):
        param = getData(request)
        res = {}
        if not param.get('api-key'):
            res['msg'] = 'api key not valid'
            return HttpResponse(json.dumps(res), status = 401)
        
        # customer = Customer.objects.filter(api_key = param.get('api-key')).first()
        if not getattr(request, 'customer'):
            res['msg'] = 'api key not valid'
            return HttpResponse(json.dumps(res), status = 401)

        return func(request, *args, **kwargs)
    
    return inner


def require_http_methods(accepted_methods: list):
    def decorator(func):
        def inner(request: WSGIRequest, *args, **kwargs):
            res = {}
            print(request.method, accepted_methods)
            if not request.method in accepted_methods:
                res['message'] = 'method not allowed'
                res['success'] = False
                return HttpResponse(json.dumps((res)), status = 405)
            
            return func(request, *args, **kwargs)
        
        return inner
    return decorator