from django_random_api.settings import IMGBB_TOKEN
from io import BytesIO
from module import text2gif
import requests as r, base64

def uploadImage(img, expiration = 60):
	data = {}
	data["key"] = IMGBB_TOKEN
	if expiration > 0:
		data["expiration"] = expiration
		
	imageB64 = base64.b64encode(img).decode()
	data["image"] = imageB64
	result = r.post("https://api.imgbb.com/1/upload", data = data).json()
	
	return result
	
	
		