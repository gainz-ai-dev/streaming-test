from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel


# Model only for User. Should have more in future. 
class User(BaseModel):
    id: str
    name: str
    email: str
    password: str


class Login(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str