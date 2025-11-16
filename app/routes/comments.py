from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentResponse

router = APIRouter()

@router.post("/", response_model=CommentResponse)
def create_comment(
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == comment_data.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    comment = Comment(
        **comment_data.dict(),
        user_id=current_user.id
    )
    
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    return comment

@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    # Faqat comment muallifi yoki loyiha muallifi o'chira oladi
    if comment.user_id != current_user.id and comment.project.inventor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    db.delete(comment)
    db.commit()
    
    return {"message": "Comment deleted successfully"}