from .text2img import text2img
from .text2sound import  text2sound
from .wiki import wikipedia
from .write import write
from .convertImgToBase64 import convertImgToBase64
from .math import generateQuestion
from .text2gif import text2gif

import os
if not os.path.exists("temp"):
	os.mkdir("temp")