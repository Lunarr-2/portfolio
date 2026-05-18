from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated


from schema import AdminPublic, AdminCreate, Token
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
import models
from auth import create_access_token, verify_password, hash_password
from datetime import timedelta
from config import settings


router = APIRouter()

@router.get("",
            response_model=list[AdminPublic],
            status_code=status.HTTP_200_OK)
async def get_all_admins(db : Annotated[AsyncSession,
                                        Depends(get_db)]):

    result = await db.execute(select(models.Admin))

    all_admin = result.scalars().all()

    return all_admin



@router.post("",
            response_model=AdminPublic,
            status_code=status.HTTP_201_CREATED)
async def create_admin(
    admin: AdminCreate,
    db: Annotated[AsyncSession, Depends(get_db)]):

    result = await db.execute(
        select(models.Admin).where(func.lower(models.Admin.email) == admin.email.lower()))


    existing_admin = result.scalars().first()

    if existing_admin :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    new_admin = models.Admin(
        username = admin.username,
        email = admin.email,
        hashed_password = hash_password(admin.password)
    )


    db.add(new_admin)
    await db.commit()
    await db.refresh(new_admin)

    return new_admin


@router.post("/login", 
             response_model=Token,
             status_code=status.HTTP_200_OK,
             summary="Admin Login ")
async def admin_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                     db: Annotated[AsyncSession, Depends(get_db)]):
    
    result = await db.execute(select(models.Admin).
                              where(func.lower(models.Admin.email) == form_data.username.lower() ))
    
    existing_admin = result.scalars().first()

    if not existing_admin or not verify_password(form_data.password, existing_admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details="Invalid Credentials",
             headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires =  timedelta(
        minutes=settings.access_token_expire_minutes
    )

    access_token = create_access_token(
        data={"sub": str(existing_admin.id)} ,
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token,token_type="bearer")