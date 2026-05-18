# def main():
#     print("Hello from professional-portfolio-website!")


# if __name__ == "__main__":
#     main()

import os
from fastapi import FastAPI, Request, status, HTTPException
from database import engine, Base
from contextlib import asynccontextmanager

from routes import admin, post, contact

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
      # Creates all tables on startup if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

# ALLOWED_ORIGINS = os.environ.get(
#     "ALLOWED_ORIGINS",
#     "http://localhost:3000,http://localhost:5500"  # default for local dev
# ).split(",")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=ALLOWED_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(post.router, prefix="/api/posts", tags=["posts"])
app.include_router(contact.router, prefix="/api/contact", tags=["contact"])

app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.get("/home")
# def get_home():
#     return {"You've gotten throught to the backend of my portfolio app"}

@app.get("/")
def frontend():
    return FileResponse("static/html/portfolio_page.html")

@app.get("/resume")
async def download_resume():
    file_path = "static/resume/resume.pdf"


    if not os.path.exists(file_path):
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="This file does not exist"
        )
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename="Tolu_Taiwo_Resume.pdf"
    )

