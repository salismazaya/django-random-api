from asyncio.staggered import staggered_race
from ninja import Schema
from typing import List, Optional

class ChangePasswordSchema(Schema):
    password: str
    new_password: str


class ChangePasswordSchemaOut(Schema):
    sucess: bool


class WriteSchema(Schema):
    text: str


class ImageSchemaOut(Schema):
    message: str
    success: bool
    base64_images: List[str]
    format: str


class Text2ImgSchema(WriteSchema):
    bgColor: str = '0,0,0,0'
    textColor: str = '255,255,255,255'
    outlineColor: str = '0,0,0,255'