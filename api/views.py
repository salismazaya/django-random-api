from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from api.decorators import api_key_required, require_http_methods
from api.utils import getData, error
import re, json, base64, module
	
@csrf_exempt
@require_http_methods(['PUT'])
@api_key_required
def change_api_key(request: WSGIRequest):
	res = {}
	new_api_key = get_random_string()
	request.customer.api_key = new_api_key
	request.customer.save()

	res['message'] = 'Success!'
	res['success'] = True
	res['new_api_key'] = new_api_key
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
	
	try:
		image_decoded = base64.b64decode(param.get('image'))
	except:
		return error('image not valid', 400)

	try:
		image = module.remove_bg(image_decoded)
		url = module.uploadImage(image, expiration = 60)['data']['url']
	except:
		return error('image not valid', 400)
	
	res['message'] = 'Success!'
	res['success'] = True
	res['image'] = url

	return HttpResponse(json.dumps(res))
