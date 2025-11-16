from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.user import UserResponse

class ProjectBase(BaseModel):
    title: str
    description: str
    short_description: str
    target_amount: float
    deadline: datetime
    category: str
    image_url: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    target_amount: Optional[float] = None
    deadline: Optional[datetime] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: int
    current_amount: float
    status: str
    inventor_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    inventor: UserResponse
    
    class Config:
        from_attributes = True

class ProjectWithStats(ProjectResponse):
    total_donations: int
    total_likes: int
    total_comments: int