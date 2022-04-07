from django.core.handlers.wsgi import WSGIRequest
from django.conf import settings
from django.http import HttpResponse
from main.models import Token
from api.models import Visitor
# from api.urls import endpoints
from ipware import get_client_ip
import json, time, requests, re

class AuthInsertVistorErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        if not request.path.startswith('/api') or re.match(r'^/api/?(docs|openapi.json)?/?$', request.path):
            return self.get_response(request)

        if not request.headers.get('Authorization') or not request.headers.get('Authorization').startswith('Bearer '):
            # return HttpResponse(json.dumps({
            #     'detail': 'Unauthorized',
            # }, indent = 4), status = 401)
            return self.get_response(request)

        start_time = time.time()
        token = request.headers['Authorization'].replace('Bearer ', '')
        token_obj = Token.objects.filter(
            token = token
        ).first()
        if not token_obj:
            # return HttpResponse(json.dumps({
            #     'detail': 'Unauthorized',
            # }, indent = 4), status = 401)
            return self.get_response(request)

        else:
            ip, _ = get_client_ip(request)
            user = token_obj.user
            request.user = user
            response = self.get_response(request)

            response_geo = requests.get('http://ip-api.com/json/{}'.format(ip)).json()
            if response_geo['status'] == 'success':
                country_code = response_geo['countryCode']
            else:
                country_code = None
            
            endpoint = request.path.replace('/api/', '')

            visitor = Visitor(
                user = user,
                endpoint = endpoint,
                ip = ip,
                country_code = country_code,
                success = not response.status_code == 500,
                proccess_time = round(time.time() - start_time, 4),
            )
            visitor.save()
                
            return response

        # return self.get_response(request)
    
    def process_exception(self, request: WSGIRequest, e):
        if not request.path.startswith('/api'):
            raise e
        
        if settings.DEBUG:
            raise e

        res = {}
        res['detail'] = str(e)
        return HttpResponse(json.dumps(res, indent = 4), status = 500)


# def auth_and_insert_visitor(get_response):
#     def middleware(request: WSGIRequest):
#         param = getData(request)

#         if not request.path.startswith('/api'):
#             return get_response(request)

#         if not request.headers['Authorization'] or not request.headers['Authorization'].startswith('Token '):
#             return get_response(request)

#         token = request.headers['Authorization'].replace('Token ', '')
#         token_obj = Token.objects.filter(
#             token = token
#         ).first()
#         if token_obj:
#             ip, _ = get_client_ip(request)
#             user = token_obj.user
#             visitor = Visitor(
#                 user = user,
#                 endpoint = request.path,
#                 ip = ip,
#             )
#             visitor.save()
#             request.user = user

#         return get_response(request)

#     return middleware

