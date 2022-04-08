from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from api.utils import getData, error
from ninja import NinjaAPI
from main.models import Token
from api.models import Visitor
from api.schemas import AudioSchemaOut, ChangePasswordSchema, ChangePasswordSchemaOut, MathSchemaOut, Text2GifSchema, Text2ImgSchema, Text2SoundSchema, WikipediaSchema, WikipediaSchemaOut, WriteSchema, ImageSchemaOut
from ninja.security import HttpBearer
from datetime import datetime
from ipware import get_client_ip
import re, json, base64, requests as r, module, hashlib, time, requests

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        return request.user

api = NinjaAPI(
	auth = AuthBearer(),
	title = 'Random API',
	version = '2.0.0'
)

@api.put('/change-token')
def change_token(request: WSGIRequest):
	res = {}

	new_token = hashlib.sha256(datetime.now().strftime("%m%d%Y%H%M%S%f" + str(request.user.id)).encode()).hexdigest()
	token = Token.objects.get(
		user__id = request.user.id
	)
	token.token = new_token
	token.save()

	res['message'] = 'Success!'
	res['success'] = True
	res['new_token'] = new_token
	return HttpResponse(json.dumps(res))

@api.put('/change-password', response = {200: ChangePasswordSchemaOut})
def change_password(request: WSGIRequest, data: ChangePasswordSchema):
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


@api.post('/write', response = {200: ImageSchemaOut})
def write(request: WSGIRequest, data: WriteSchema):
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
        res['base64_images'] = list(map(lambda img: module.convertImgToBase64(img), result))
        res['format'] = 'jpg'
    
    return HttpResponse(json.dumps(res), status = status)

@api.post('/text2img', response = {200: ImageSchemaOut})
def text2img(request: WSGIRequest, data: Text2ImgSchema):
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
	# url = module.uploadImage(img, expiration = 60)['data']['url']
	base64_image = module.convertImgToBase64(img)
	
	res['message'] = 'Success!'
	res['success'] = True
	res['base64_images'] = [base64_image]
	res['format'] = 'png'
	
	return HttpResponse(json.dumps(res))


@api.get('/wikipedia', response = {200: WikipediaSchemaOut})
def wikipedia(request: WSGIRequest, data: WikipediaSchema):
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

@api.get('/math', response = {200: MathSchemaOut})
def math(request: WSGIRequest):
	res = {}
	img, answer = module.generateQuestion()
	base64_img = module.convertImgToBase64(img)

	res['message'] = 'Success!'
	res['success'] = True
	res['base64_images'] = [base64_img]
	res['format'] = 'jpg'
	res['answer'] = int(answer)
	return HttpResponse(json.dumps(res))


@api.post('/text2gif', response = {200: ImageSchemaOut})
def text2gif(request: WSGIRequest, data: Text2GifSchema):
	res = {}
	param = getData(request)
	
	if not param.get('text'):
		return error('no text!', 400)
	
	bgColor = param.get('bgColor')
	if not bgColor:
		bgColor = (0, 0, 0, 0)
	elif re.match(r'^\d{1,3},\d{1,3},\d{1,3},\d{1,3}$', bgColor):
		bgColor = tuple(int(x) for x in bgColor.split(','))
	else:
		return error('bgColor not valid', 400)

	gif = module.text2gif(param['text'], bgColor = bgColor)
	base64_gif = module.convertImgToBase64(gif)
	
	res['message'] = 'Success!'
	res['success'] = True
	res['base64_images'] = [base64_gif]
	res['format'] = 'gif'

	return HttpResponse(json.dumps(res))


@api.post('/text2sound', response = {200: AudioSchemaOut})
def text2sound(request: WSGIRequest, data: Text2SoundSchema):
	res = {}
	data = getData(request)
	
	if not data.get("text"):
		raise error("Mohon masukan text!", 400)
	if not data.get("languageCode"):
		return error("Mohon masukan languageCode", 400)
	
	languageCode = data["languageCode"]
	
	try:
		result = module.text2sound(data["text"][:150], languageCode = languageCode)
	except ValueError:
		return error(f"kode bahasa '{languageCode}' tidak ditemukan", 400)

	base64_audio = base64.b64encode(result).decode()
		
	# def generate():
	# 	result.seek(0)
	# 	data = result.read(1024)
		
	# 	while data:
	# 		yield data
	# 		data = result.read(1024)

	
	res['message'] = 'Success!'
	res['success'] = True
	res['base64_audios'] = [base64_audio]
	res['format'] = 'opus'
	
	return HttpResponse(json.dumps(res))