from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.like import Like

router = APIRouter()

@router.post("/projects/{project_id}/like")
def like_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Like mavjudligini tekshirish
    existing_like = db.query(Like).filter(
        Like.user_id == current_user.id,
        Like.project_id == project_id
    ).first()
    
    if existing_like:
        # Like ni olib tashlash (unlike)
        db.delete(existing_like)
        db.commit()
        return {"message": "Project unliked successfully"}
    else:
        # Yangi like qo'shish
        like = Like(user_id=current_user.id, project_id=project_id)
        db.add(like)
        db.commit()
        return {"message": "Project liked successfully"}

@router.get("/projects/{project_id}/likes/count")
def get_likes_count(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    likes_count = db.query(Like).filter(Like.project_id == project_id).count()
    return {"likes_count": likes_count}