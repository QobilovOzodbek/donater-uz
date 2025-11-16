from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserResponse,Optional

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    project_id: int

class CommentResponse(CommentBase):
    id: int
    user_id: int
    project_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user: UserResponse
    
    class Config:
        from_attributes = True