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


class Text2GifSchema(WriteSchema):
    bgColor: str = '0,0,0,0'


class Text2ImgSchema(Text2GifSchema):
    textColor: str = '255,255,255,255'
    outlineColor: str = '0,0,0,255'


class Text2SoundSchema(WriteSchema):
    languageCode: str = 'id'


class AudioSchemaOut(Schema):
    message: str
    success: bool
    base64_audios: List[str]
    format: str

class WikipediaSchema(Schema):
    query: str


class WikipediaSchemaOut(Schema):
    message: str
    success: bool
    title: str
    content: str

class MathSchemaOut(ImageSchemaOut):
    answer: int