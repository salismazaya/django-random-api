import random

def sortTextLines(text, maxTextPerLine):
	finalText = []
	tempText = []
	for x in text.split("\n"):
		for  y in x.split(" "):
			lenTempText = " ".join(tempText)
			lenTempText = len(lenTempText)
			
			if type(maxTextPerLine) in [list, tuple]:
				maxTextPerLine_ = random.randint(*maxTextPerLine)
			else:
				maxTextPerLine_ = maxTextPerLine
				
			if lenTempText + len(y) > maxTextPerLine_:
				finalText.append(" ".join(tempText))
				tempText = []
					
			tempText.append(y)
	
		if tempText:
			finalText.append(" ".join(tempText))
			tempText = []
	
	return finalText