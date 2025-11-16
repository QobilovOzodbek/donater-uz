from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.user import UserResponse
from app.schemas.project import ProjectResponse

class DonationBase(BaseModel):
    amount: float
    message: Optional[str] = None
    is_anonymous: bool = False

class DonationCreate(DonationBase):
    project_id: int

class DonationResponse(DonationBase):
    id: int
    donator_id: int
    project_id: int
    created_at: datetime
    donator: Optional[UserResponse] = None
    project: Optional[ProjectResponse] = None
    
    class Config:
        from_attributes = True