from .text2img import text2img
from .text2sound import  text2sound
from .wiki import wikipedia
from .write import write
from .uploadImage import uploadImage
from .math import generateQuestion
from .text2gif import text2gif
from .remove_bg import remove_bg

import os
if not os.path.exists("temp"):
	os.mkdir("temp")