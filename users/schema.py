from ninja import Schema
from pydantic import EmailStr

class LoginSchema(Schema):
    username: str
    password: str

class UserIn(Schema):
    username: str
    password: str
    email: EmailStr