from typing import Optional

from pydantic import BaseModel, Field, Base64Bytes
from enums import Genre


class AddAudiobook(BaseModel):
    author: int = Field()
    title: str = Field(max_length=30)
    description: str = Field(max_length=700)
    genre: Genre
    is_mature_content: bool
    file: Base64Bytes


class EditAudiobook(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    genre: Optional[str] = None
    is_mature_content: Optional[bool] = None
    file: Optional[Base64Bytes] = None
    rating: Optional[float] = None
