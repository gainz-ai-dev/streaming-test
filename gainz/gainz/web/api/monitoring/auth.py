import jwt
import time
import os
import bcrypt
import json
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from gainz.settings import Settings
from .db import get_db, get_collection
from .model import User, Login, Token, Thread
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.environ.get("JWT_SECRET")
ALGORITHM = "HS256"

# JWT function
# Currently, it's only a very very very prelimit JWT development. Use 3rd party provider and cloud solution is recommended. 
def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = int(time.time() + 6000)  # Token expiry in seconds
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token):
    try:
        secret_key = JWT_SECRET
        decoded_token = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError: 
        return "Token expired"
    except jwt.InvalidTokenError:
        return "Invalid token"
    
def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        user = get_user_by_id(user_id) 
        if user is None:
            raise credentials_exception
        return user
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    
def get_password_hash(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# User Management function
def get_user_by_id(user_id: int):
    db = get_db()
    collection = db['User']
    user = collection.find_one({"id": user_id})

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Protected route
auth = APIRouter()

@auth.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: User):
    # Hash the password before storing
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    db = get_db()
    collection = db['User']
    user_data = vars(user)
    user_data['_id']= user.id
    collection.insert_one(user_data)
    return {"message": "User created successfully"}

# To Do. Should send fail message 


@auth.post("/login")
async def login_user(login: Login):
    email = login.email     
    db = get_db()
    collection = db['User']
    user = collection.find_one({"email": email})

    if not user:
        return {"message": "Login unsuccessful"}

    if not bcrypt.checkpw(login.password.encode('utf-8'), user["password"]):
        return {"message": "Login unsuccessful"}

    else:
        data = {"user_id": user['id']}
        access_token = create_access_token(data)
        verify_token(access_token)
        return {"access_token": access_token,"user_id":user['id'], "token_type": "bearer"}

# This is internal check the users stored in DB. You will see in console log of backend.
@auth.get("/list")
def seed_initial_data():
    db = get_db()
    collection = db['Thread']
    for x in collection.find():
        print(x)
    return {"message": "All User List"}

# This is to check the API is authenticated for using. 
# To Do. Currently, it is a one off check. It should be embeded authentication to all API. 
@auth.post("/protected_route")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user['name']}!"}

@auth.get("/create")
def create_initial_data():
    return True
