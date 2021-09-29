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
            param.update(data)
        except:
            pass

    return param


def error(msg, status):
    res = {}
    res['message'] = msg
    res['success'] = False
    
    return HttpResponse(json.dumps(res), status = status)