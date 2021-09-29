from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from .sorting import sortTextLines
from io import BytesIO
import random, os

SIZE_IMG = (500, 500)
MAX_TEXT_PER_LINE = 16

def text2gif(text, padding = 5, margin = 50, bgColor = (0, 0, 0, 100)):
	texts = sortTextLines(text, MAX_TEXT_PER_LINE)
	keren = "\n".join(texts)
	
	fontSize = 35
	font = ImageFont.truetype("files/fonts/LazyMeow-Demo.otf", fontSize)
	while font.getsize_multiline(keren)[0] + margin < SIZE_IMG[0] and font.getsize_multiline(keren)[1] + margin < SIZE_IMG[1]:
		fontSize += 5
		font = ImageFont.truetype("files/fonts/LazyMeow-Demo.otf", fontSize)
	
	def generate(textColor):
		img = Image.new("RGBA", SIZE_IMG, bgColor)
		draw = ImageDraw.Draw(img)
		yPosition = (SIZE_IMG[1] - draw.textsize("\n".join(texts), font = font)[1]) // 2
		yPosition -= (len(texts) -1) * padding
		
		for text in texts:
			sizeText = draw.textsize(text, font = font)
			xPosition = (SIZE_IMG[0] - sizeText[0]) // 2
			draw.text((xPosition, yPosition), text, font = font, fill = textColor)
			yPosition += sizeText[1] + padding
		
		
		filePath = f"temp/{random.randint(0, 100000)}.png"
		img.save(filePath)
		return filePath

	colors = ["red", "blue", "black", "purple", "yellow"]
	imagesPath = list(map(generate, colors))
	filePath = f"temp/{random.randint(0, 100000)}.gif"

	os.system(f"convert -delay 20 {' '.join(imagesPath)} -loop 5 {filePath}")
	rv = open(filePath, "rb").read()
	for imagePath in imagesPath:
		os.remove(imagePath)

	os.remove(filePath)

	return rv