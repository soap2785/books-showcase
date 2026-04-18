from typing import Optional

from pydantic import BaseModel, Field


class CreateAuthor(BaseModel):
    fullname: str = Field(max_length=63)
    description: str = Field(max_length=700)


class EditAuthor(BaseModel):
    fullname: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
