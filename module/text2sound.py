from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment

def text2sound(text, languageCode, convertToOpus = True):
	audio = BytesIO()
	gtts = gTTS(text, lang = languageCode)
	gtts.write_to_fp(audio)
	
	if convertToOpus:
		audioOpus = BytesIO()
		audio.seek(0)
		AudioSegment.from_file(audio).export(audioOpus, format = "opus")
		return audioOpus.getvalue()
	
	return audio.getvalue()