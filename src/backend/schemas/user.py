from pydantic import BaseModel, Field, EmailStr


class Authenticate(BaseModel):
    username: str = Field()
    email: str = EmailStr()
    password: str = Field()


class DeleteUser(BaseModel):
    id: int = Field()
    password: str = Field()
