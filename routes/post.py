from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from database import get_db
from schema import PostCreate, PostResponse, PostUpdate
import models
from auth import CurrentAdmin


router = APIRouter()

@router.post("",
            response_model=PostResponse,
            status_code= status.HTTP_201_CREATED,
            summary="Creating a new post")
async def create_post(post: PostCreate,
                      current_admin: CurrentAdmin,
                      db: Annotated[AsyncSession, Depends(get_db)]):
    
    if not current_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have permission to create a post"
        )
    
    new_post =  models.Post(
        title= post.title ,
        description= post.description ,
        github_link= post.github_link,
        tools= post.tools,
        admin_id= current_admin.id
    )

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    return new_post


@router.get("", 
            response_model=list[PostResponse],
            status_code=status.HTTP_200_OK, 
            summary="Getting all the posts")
async def get_all_post(db: Annotated[AsyncSession, Depends(get_db)]):

    result = await db.execute(select(models.Post))

    all_post = result.scalars().all()

    return all_post


@router.patch("/{post_id}", response_model=PostResponse, 
              status_code=status.HTTP_200_OK, 
              summary="Updating an Existing post")
async def post_partial_update(
                                post_id: int,
                                post: PostUpdate,
                                db: Annotated[AsyncSession, Depends(get_db)]):
    
    result = await db.execute(select(models.Post).where(models.Post.id == post_id))

    existing_post= result.scalars().first()

    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This post does not exist"
        )
    # existing_post.title = post.title
    # existing_post.description= post.description 
    # existing_post.github_link= post.github_link
    # existing_post.tools = post.tools

     # Only get the fields the client actually sent
    update_data = post.model_dump(exclude_unset=True)

    # Only update those specific fields on the existing post
    for field, value in update_data.items():
        setattr(existing_post, field, value)

   

    await db.commit()
    await db.refresh(existing_post)

    return existing_post


@router.delete("/{post_id}", 
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Deleting a post")
async def delete_post(post_id: int,
                      db: Annotated[AsyncSession, Depends(get_db)]):
    
    result = await db.execute(select(models.Post).where(models.Post.id == post_id))

    current_post = result.scalars().first()

    await db.delete(current_post)
    await db.commit()
