import random
import re
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def generateQuestion():
	question = generateRawQuestion()
	text = "\n".join(question[0])

	img = Image.new('RGB', (600, 500), color = 'white')
	font = ImageFont.truetype("files/fonts/Locanita.ttf", 70)

	draw = ImageDraw.Draw(img)
	w, h = draw.textsize(text, font = font)

	xPosition = (600 - w) // 2
	yPosition = (500 - h) // 2
	draw.text((xPosition, yPosition), text, (45, 56, 61), font = font)

	imgBytes = BytesIO()
	img.save(imgBytes, format = "JPEG")
	return imgBytes.getvalue(), question[1]

def generateRawQuestion():
	alpha = {
		"A":random.randint(1,50),
		"B":random.randint(1,60),
		"C":random.randint(1,70),
	}

	data = []

	def random_alpha():
		return random.choice(list(alpha.items()))

	def generateLine():
		n1 = random_alpha()
		n2 = random_alpha() 
		n3 = random_alpha()
		n4 = random_alpha()

		o1 = random.choice(["-", "+"])
		o2 = random.choice(["-", "+"])
		o3 = random.choice(["-", "+"])

		raw_number = f"{n1[0]} {o1} {n2[0]} {o2} {n3[0]} {o3} {n4[0]}"
		number = f"{n1[1]} {o1} {n2[1]} {o2} {n3[1]} {o3} {n4[1]}"

		total = str(eval(number))

		raw_number = f"{raw_number} = {total}"

		return raw_number

	for _ in range(5):
		angka = generateLine()
		data.append(angka)

	question = generateLine()
	answer = question.split(" = ")[1]
	question = re.sub(r"=.+", "= ??", question)
	data.append(question)

	return data, answer
