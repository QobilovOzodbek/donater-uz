from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import List, Optional
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.donation import Donation
from app.models.comment import Comment
from app.models.like import Like
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.schemas.donation import DonationResponse
from app.schemas.comment import CommentResponse

router = APIRouter()

@router.post("/", response_model=ProjectResponse)
def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_inventor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only inventors can create projects"
        )
    
    project = Project(
        **project_data.dict(),
        inventor_id=current_user.id
    )
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return project

@router.get("/", response_model=List[ProjectResponse])
def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Project)
    
    if category:
        query = query.filter(Project.category == category)
    
    if status:
        query = query.filter(Project.status == status)
    
    projects = query.offset(skip).limit(limit).all()
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if project.inventor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    for field, value in project_data.dict(exclude_unset=True).items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    return project

@router.get("/{project_id}/donations", response_model=List[DonationResponse])
def get_project_donations(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    donations = db.query(Donation).filter(Donation.project_id == project_id).all()
    return donations

@router.get("/{project_id}/comments", response_model=List[CommentResponse])
def get_project_comments(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    comments = db.query(Comment).filter(Comment.project_id == project_id).all()
    return comments