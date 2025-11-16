from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import user, project, donation, comment, like
from app.routes import (
    auth_router, 
    users_router, 
    projects_router, 
    donations_router, 
    comments_router, 
    likes_router
)

# Ma'lumotlar bazasi jadvallarini yaratish
user.Base.metadata.create_all(bind=engine)
project.Base.metadata.create_all(bind=engine)
donation.Base.metadata.create_all(bind=engine)
comment.Base.metadata.create_all(bind=engine)
like.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Invention Platform API",
    description="Ixtiro va loyiha moliyalashtirish platformasi",
    version="1.0.0"
)

# CORS sozlamalari
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routelarni qo'shish
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(projects_router, prefix="/projects", tags=["Projects"])
app.include_router(donations_router, prefix="/donations", tags=["Donations"])
app.include_router(comments_router, prefix="/comments", tags=["Comments"])
app.include_router(likes_router, prefix="/likes", tags=["Likes"])

@app.get("/")
async def root():
    return {"message": "Invention Platform API ishga tushdi!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}