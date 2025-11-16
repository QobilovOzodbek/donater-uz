from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    short_description = Column(String(500), nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    deadline = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(50), default="active")
    category = Column(String(100), nullable=False)
    image_url = Column(String(500), nullable=True)
    inventor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    inventor = relationship("User", back_populates="projects")
    donations = relationship("Donation", back_populates="project")
    comments = relationship("Comment", back_populates="project")
    likes = relationship("Like", back_populates="project")