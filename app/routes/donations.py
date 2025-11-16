from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.donation import Donation
from app.schemas.donation import DonationCreate, DonationResponse

router = APIRouter()

@router.post("/", response_model=DonationResponse)
def create_donation(
    donation_data: DonationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == donation_data.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if project.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project is not active"
        )
    
    donation = Donation(
        **donation_data.dict(),
        donator_id=current_user.id
    )
    
    # Loyihaning joriy summasini yangilash
    project.current_amount += donation_data.amount
    
    db.add(donation)
    db.commit()
    db.refresh(donation)
    
    return donation

@router.get("/{donation_id}", response_model=DonationResponse)
def get_donation(
    donation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found"
        )
    
    # Faqat o'z donation'ini yoki loyiha muallifi ko'ra oladi
    if donation.donator_id != current_user.id and donation.project.inventor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return donation