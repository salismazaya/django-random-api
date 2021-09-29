from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from .sorting import sortTextLines
from io import BytesIO

SIZE_IMG = (500, 500)
MAX_TEXT_PER_LINE = 16

def text2img(text, padding = 5, margin = 50, bgColor = (0, 0, 0, 100), textColor = "white", outlineColor = "black"):
	img = Image.new("RGBA", SIZE_IMG, bgColor)
	draw = ImageDraw.Draw(img)
	texts = sortTextLines(text, MAX_TEXT_PER_LINE)
	keren = "\n".join(texts)
	
	fontSize = 35
	font = ImageFont.truetype("files/fonts/SFDistantGalaxy.ttf", fontSize)
	while font.getsize_multiline(keren)[0] + margin < SIZE_IMG[0] and font.getsize_multiline(keren)[1] + margin < SIZE_IMG[1]:
		fontSize += 5
		font = ImageFont.truetype("files/fonts/SFDistantGalaxy.ttf", fontSize)
	
	yPosition = (SIZE_IMG[1] - draw.textsize("\n".join(texts), font = font)[1]) // 2
	yPosition -= (len(texts) -1) * padding
	
	fontOutline = ImageFont.truetype("files/fonts/SFDistantGalaxyOutline.ttf", fontSize)
	
	for text in texts:
		sizeText = draw.textsize(text, font = font)
		xPosition = (SIZE_IMG[0] - sizeText[0]) // 2
		draw.text((xPosition, yPosition), text, font = font, fill = textColor)
		draw.text((xPosition, yPosition), text, font = fontOutline, fill = outlineColor)
		yPosition += sizeText[1] + padding
	
	rv = BytesIO()
	img.save(rv, format = "PNG")
	return rv.getvalue()