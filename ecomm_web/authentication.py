from passlib.context import CryptContext
import jwt

from datetime import datetime, timedelta
from fastapi import FastAPI, Depends,  Request, HTTPException, status
from fastapi.security import *
from authentication import security
from authentication import get_user_from_db

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username, password):
    # Replace with your logic to fetch user from the database
    user = get_user_from_db(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return True


def create_access_token(username):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        return username
    except jwt.JWTError:
        return None


def get_current_user(token: str = Depends(security)):
    username = decode_access_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return username