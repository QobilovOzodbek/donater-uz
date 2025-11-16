from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.projects import router as projects_router
from app.routes.donations import router as donations_router
from app.routes.comments import router as comments_router
from app.routes.likes import router as likes_router

__all__ = [
    "auth_router",
    "users_router", 
    "projects_router",
    "donations_router",
    "comments_router",
    "likes_router"
]