from os import stat
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
import json

def getData(request: WSGIRequest):
    param = request.GET.copy()
    param.update(request.POST)

    if request.is_ajax:
        try:
            data = json.loads(request.body.decode())
        except:
            data = dict([x.split('=') for x in request.body.decode().split('&')])
        param.update(data)


    return param


def error(msg, status):
    res = {}
    res['detail'] = msg
    
    return HttpResponse(json.dumps(res), status = status)