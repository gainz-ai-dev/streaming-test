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

class Message(BaseModel):
    id: str
    tid: str
    msg: str
    timestamp: int

class Thread(BaseModel):
    id:str
    aid: str
    uid: str
    timestamp: int