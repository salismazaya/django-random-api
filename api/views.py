from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from api.decorators import api_key_required, require_http_methods
from api.utils import getData, error
import re, json, base64, requests as r, module
	
@csrf_exempt
@require_http_methods(['PUT'])
@api_key_required
def change_api_key(request: WSGIRequest):
	res = {}
	param = getData(request)

	if not param.get('password'):
		return error('no password', 400)

	user: User = request.customer.user
	if not user.check_password(param.get('password')):
		return error('wrong password', 401)

	new_api_key = get_random_string()
	request.customer.api_key = new_api_key
	request.customer.save()

	res['message'] = 'Success!'
	res['success'] = True
	res['new_api_key'] = new_api_key
	return HttpResponse(json.dumps(res))


@csrf_exempt
@require_http_methods(['PUT'])
@api_key_required
def change_password(request: WSGIRequest):
	res = {}
	param = getData(request)
	new_password = param.get('new-password')
	user: User = request.customer.user

	if not param.get('password'):
		return error('no password', 400)
	
	if not new_password:
		return error('no new-password', 400)

	if len(new_password) < 5 or len(new_password) > 20:
		return error('password min 5, max 20', 400)
	
	if not user.check_password(param.get('password')):
		return error('wrong password', 401)
	
	user.set_password(param.get('new-password'))
	user.save()

	res['success'] = True
	return HttpResponse(json.dumps(res))


@csrf_exempt
@require_http_methods(['POST'])
@api_key_required
def write(request: WSGIRequest):
    res = {}
    param = getData(request)

    if not param.get('text'):
        status = 400
        res['message'] = 'no text'
        res['success'] = False
    else:
        result = module.write(param['text'])
        status = 200
        res['message'] = 'Success!'
        res['success'] = True
        res['images'] = list(map(lambda img: module.uploadImage(img, expiration = 60)['data']['url'], result))

    return HttpResponse(json.dumps(res), status = status)

@csrf_exempt
@api_key_required
def text2img(request: WSGIRequest):
	res = {}
	param = getData(request)
	
	if not param.get('text'):
		return error('no text', 400)
	
	bgColor = param.get('bgColor')
	if not bgColor:
		bgColor = (0, 0, 0, 0)
	elif re.match(r'^\d{1,3},\d{1,3},\d{1,3},\d{1,3}$', bgColor):
		bgColor = tuple(int(x) for x in bgColor.split(','))
	else:
		return error('bgColor not valid', 400)
	
	textColor = param.get('textColor')
	if not textColor:
		textColor = 'white'

	elif re.match(r'^\d{1,3},\d{1,3},\d{1,3},\d{1,3}$', textColor):
		textColor = tuple(int(x) for x in textColor.split(','))
	else:
		return error('textColor not valid', 400)
		
	outlineColor = param.get('outlineColor')
	if not outlineColor:
		outlineColor = 'black'
	elif re.match(r'^\d{1,3},\d{1,3},\d{1,3},\d{1,3}$', outlineColor):
		outlineColor = tuple(int(x) for x in outlineColor.split(','))
	else:
		return error('outlineColor not valid', 400)
	
	img = module.text2img(param['text'], bgColor = bgColor, textColor = textColor, outlineColor = outlineColor)
	url = module.uploadImage(img, expiration = 60)['data']['url']
	
	res['message'] = 'Success!'
	res['success'] = True
	res['image'] = url
	
	return HttpResponse(json.dumps(res))

@csrf_exempt
@require_http_methods(['POST'])
@api_key_required
def remove_bg(request: WSGIRequest):
	res = {}
	param = getData(request)
	
	if not param.get('image'):
		return error('no image', 400)

	# if not re.match(r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$', param.get('image')):
	if True:
		try:
			image_decoded = base64.b64decode(param.get('image'))
		except:
			return error('image not valid', 400)

		if len(image_decoded) > 1048576:
			return error('maximal file size 1mb', 400)
	
	# else:
	# 	image_decoded = r.get(param.get('image')).content

	# 	if len(image_decoded) > 1048576:
	# 		return error('maximal file size 1mb', 400)

	try:
		image = module.remove_bg(image_decoded)
		url = module.uploadImage(image, expiration = 60)['data']['url']
	except:
		return error('image not valid', 400)
	
	res['message'] = 'Success!'
	res['success'] = True
	res['image'] = url

	return HttpResponse(json.dumps(res))


@csrf_exempt
@require_http_methods(['GET'])
@api_key_required
def wikipedia(request: WSGIRequest):
	res = {}
	param = getData(request)

	if not param.get('query'):
		return error('no query', 400)
	
	result = module.wikipedia(param['query'])
	if not result.get('success'):
		return error('article not found', 404)
	
	res['message'] = 'Success!'
	res['success'] = True
	res['title'] = result['title']
	res['content'] = result['content']

	return HttpResponse(json.dumps(res))

@csrf_exempt
@require_http_methods(['GET'])
@api_key_required
def math(request: WSGIRequest):
	res = {}
	img, answer = module.generateQuestion()
	url = module.uploadImage(img)['data']['url']

	res['message'] = 'Success!'
	res['success'] = True
	res['image'] = url
	res['answer'] = int(answer)
	return HttpResponse(json.dumps(res))


@csrf_exempt
@require_http_methods(['POST'])
@api_key_required
def text2gif(request: WSGIRequest):
	res = {}
	param = getData(request)
	
	if not param.get('text'):
		raise error('no text!', 400)
	
	bgColor = param.get('bgColor')
	if not bgColor:
		bgColor = (0, 0, 0, 0)
	elif re.match(r'^\d{1,3},\d{1,3},\d{1,3},\d{1,3}$', bgColor):
		bgColor = tuple(int(x) for x in bgColor.split(','))
	else:
		return error('bgColor not valid', 400)

	gif = module.text2gif(param['text'], bgColor = bgColor)
	url = module.uploadImage(gif, expiration = 60)['data']['url']
	
	res['message'] = 'Success!'
	res['success'] = True
	res['image'] = url

	return HttpResponse(json.dumps(res))
	