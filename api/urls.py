from os import name
from django.urls import re_path
from api.views import change_api_key, write, text2img, remove_bg

urlpatterns = [
    re_path(r'change-api-key/?', change_api_key, name = 'api-change-api-key'),
    re_path(r'write/?', write, name = 'api-write'),
    re_path(r'text2img/?', text2img, name= 'api-text2img'),
    re_path(r'remove-bg/?', remove_bg, name = 'api-remove-bg')
]