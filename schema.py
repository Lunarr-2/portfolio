from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class AdminModel(BaseModel):
    username: str = Field(...,min_length=3,max_length=50)
    email: EmailStr = Field(..., example="user1@example.com")
    

class AdminCreate(AdminModel):
    password : str = Field(...,min_length=8, example="password123")

class AdminLogin(AdminModel):
    email: EmailStr 
    password : str = Field(...,min_length=8, example="password123")

class AdminPublic(AdminModel):
    id : int
    username: str

    model_config = {
        "from_attributes": True
    }

class AdminPrivate(AdminModel):
    id : int
    username: str
    email: EmailStr


class AdminResponse(AdminModel):
    id: int

    model_config = {
        "from_attributes": True
    }

class PostModel(BaseModel):
    title: str = Field(...,min_length=3,max_length=150,example="Project 1")
    description: str = Field(...,min_length=10,max_length=500,example="This is a description for Project 1")
    github_link : str = Field(...,min_length=3,max_length=250,example="projec1@githublink.com")
    tools: List[str] = Field(
        default=[],
        example=["Pandas", "SQL", "PowerBI"],
        description="Technologies used in the project"
    )

    model_config = {
        "from_attributes": True
    }

class PostCreate(PostModel):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None,min_length=3,max_length=150,example="Project 1")
    description: Optional[str] = Field(None,min_length=10,max_length=500,example="This is a description for Project 1")
    github_link : Optional[str] = Field(None,min_length=3,example="projec1@githublink.com")
    tools: Optional[List[str]] = Field(None)

class PostResponse(PostModel):
    id: int

    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    message: str