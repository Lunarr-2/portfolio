from typing import List
from sqlalchemy import String, Integer, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    posts: Mapped[List["Post"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
    )


class Post(Base):
    __tablename__ = "posts"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150),  nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    github_link : Mapped[str] = mapped_column(String,  nullable=False)
    tools: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    admin_id : Mapped[int] = mapped_column(
        ForeignKey("admins.id"), nullable=False, index=True)
    
    author: Mapped["Admin"] = relationship(back_populates="posts")

