from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base
from .enums import CompanyPhaseEnum

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, required=True, unique=True, index=True)
    foundation_date = Column(DateTime, nullable=True)
    industry = Column(String, nullable=True)
    size = Column(String, nullable=True)
    phase = Column(SQLAlchemyEnum(CompanyPhaseEnum), nullable=True)
    website = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    crunchbase = Column(String, nullable=True) # Column name can't be 'Crunchbase'
    glassdoor = Column(String, nullable=True)
    short_description = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    related_articles = Column(Text, nullable=True) # Stores comma-separated URLs

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    job_applications = relationship("JobApplication", back_populates="company") 