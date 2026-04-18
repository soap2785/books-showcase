from typing import Optional

from pydantic import BaseModel, Field, Base64Bytes
from enums import Genre


class AddBook(BaseModel):
    author: int = Field()
    title: str = Field(max_length=30)
    description: str = Field(max_length=700)
    genre: Genre = Field(max_length=30)
    is_mature_content: bool = Field()
    pages: int = Field()
    file: Base64Bytes = Base64Bytes()


class EditBook(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    genre: Optional[str] = None
    is_mature_content: Optional[bool] = None
    pages: Optional[int] = None
    file: Optional[Base64Bytes] = None
    rating: Optional[float] = None