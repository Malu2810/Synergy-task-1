from pydantic import BaseModel, EmailStr


class Login(BaseModel):
    username: str
    password: str


class Signup(BaseModel):
    username: str
    password: str
    email: EmailStr