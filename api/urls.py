# from django.urls import re_path
# from api.views import change_token, change_password, math, text2gif, wikipedia, write, text2img, remove_bg, text2sound
from api.views import api
import re

# urlpatterns = [
#     re_path(r'^change-password/?$', change_password, name = 'change-password'),
#     re_path(r'^change-token/?$', change_token, name = 'change-token'),
#     re_path(r'^write/?$', write, name = 'write'),
#     re_path(r'^text2img/?$', text2img, name= 'text2img'),
#     re_path(r'^remove-bg/?$', remove_bg, name = 'remove-bg'),
#     re_path(r'^wikipedia/?$', wikipedia, name = 'wikipedia'),
#     re_path(r'^math/?$', math, name = 'math'),
#     re_path(r'^text2gif/?$', text2gif, name = 'text2gif'),
#     re_path(r'^text2sound/?$', text2sound, name = 'text2sound'),
# ]
urlpatterns = api.urls

endpoints = [urlpattern.pattern._route for urlpattern in urlpatterns[0]]
endpoints.remove('')
endpoints.remove('openapi.json')
endpoints.remove('docs')
endpoints_pattern = re.compile('^/api/({})$'.format('|'.join(endpoints)))