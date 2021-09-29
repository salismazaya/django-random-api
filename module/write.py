from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from .sorting import sortTextLines
from io import BytesIO
import random

FONT = ImageFont.truetype("files/fonts/IndieFlower.ttf", 23)
TEXT_COLOR = (45, 56, 63)

def write(text):
	text = sortTextLines(text, (50, 54))
	texts = [text[i:i+25] for i in range(0, len(text), 25)][:4]
	
	def gasWrite(text):
		img = Image.open("files/images/backgroud-kertas.jpg")
		draw = ImageDraw.Draw(img)
		yPosition = 125
		
		for word in text:
			xPosition = random.randint(150, 155)
			draw.text((xPosition, yPosition), word, TEXT_COLOR, font = FONT)
			yPosition += 40
		
		rv = BytesIO()
		img.save(rv, format = "JPEG")
		return rv.getvalue()
	
	result = list(map(gasWrite, texts))
	return result