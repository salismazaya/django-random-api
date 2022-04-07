import base64

def convertImgToBase64(image: bytes) -> str:
    return base64.b64encode(image).decode()