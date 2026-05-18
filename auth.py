from pwdlib import PasswordHash
import jwt
from datetime import timedelta , datetime, UTC
from config import settings
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from database import get_db
import models




password_hasher = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/login")

def hash_password(password: str):
    return password_hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    try :
        return password_hasher.verify(plain_password, hashed_password)
    except:
        return "This Password do not match"


def create_access_token(data: dict, expires_delta: timedelta| None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else :
        expire = datetime.now(UTC) + timedelta(30)

    to_encode.update({"exp" : expire})

    encode_jwt = jwt.encode(to_encode,
                            settings.secret_key.get_secret_value(),
                            algorithm=settings.algorithm)
    
    return encode_jwt

def verify_access_token(token: str):
    
    try:
        decode_jwt = jwt.decode(token,
                                settings.secret_key.get_secret_value(),
                                algorithms=[settings.algorithm],
                                options={"require": ["sub","exp"]})
    except jwt.InvalidTokenError :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token "
        )
    else :
        return decode_jwt.get("sub")
    

async def get_current_admin(
        token: Annotated[str,Depends(oauth2_scheme)],
        db: Annotated[AsyncSession, Depends(get_db)]):
    
    admin_id = verify_access_token(token)

    if admin_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    try:

        admin_id_int = int(admin_id)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    

    result = await db.execute(
        select(models.Admin).where(models.Admin.id == admin_id_int))
    
    admin = result.scalars().first()

    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin Not Found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return admin



CurrentAdmin = Annotated[models.Admin, Depends(get_current_admin)]