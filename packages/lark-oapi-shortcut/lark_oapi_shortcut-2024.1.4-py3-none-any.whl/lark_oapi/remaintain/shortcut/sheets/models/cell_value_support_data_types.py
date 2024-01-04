from enum import Enum

from pydantic import BaseModel, Field


class TextLink(BaseModel):
    type: str = "url"
    text: str
    link: str


class Formula(BaseModel):
    type: str = "formula"
    text: str


class MentionDocObjType(Enum):
    sheet = "sheet"
    doc = "doc"
    slide = "slide"
    bitable = "bitable"
    mindnote = "mindnote"


class MentionDoc(BaseModel):
    type: str = "mention"
    text_type: str = Field('fileToken', alias='textType')
    text: str
    obj_type: MentionDocObjType = Field(MentionDocObjType.doc, alias='objType')


class MentionUser(BaseModel):
    type: str = "mention"
    text: str
    text_type: str = Field("email", alias='textType')
    notify: bool = False
    grant_read_permission: bool = Field(False, alias='grantReadPermission')
