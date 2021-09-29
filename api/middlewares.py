from django.core.handlers.wsgi import WSGIRequest
from main.models import Visitor, Customer
from api.utils import getData

def visitor(get_response):
    def middleware(request: WSGIRequest):
        param = getData(request)

        if not request.path.startswith('/api'):
            request.customer = None
            return get_response(request)

        if not param.get('api-key'):
            request.customer = None
            return get_response(request)
        
        customer = Customer.objects.filter(api_key = param.get('api-key')).first()
        if not customer:
            request.customer = None
            return get_response(request)
        
        request.customer = customer
        visitor = Visitor(
            customer = customer
        )
        visitor.save()

        return get_response(request)

    return middleware

