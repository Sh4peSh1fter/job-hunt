from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum as SQLAlchemyEnum, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base
from .enums import EmploymentTypeEnum, ApplicationStatusEnum

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    title = Column(String, nullable=False)
    description_text = Column(Text, nullable=True)
    job_url = Column(String, nullable=False)
    location_city = Column(String, nullable=True)
    location_country = Column(String, nullable=True)
    is_remote = Column(Boolean, default=False)
    employment_type = Column(SQLAlchemyEnum(EmploymentTypeEnum), nullable=True)
    
    used_resume = Column(String, nullable=True)
    cover_letter_file_path = Column(String, nullable=True)
    
    requested_salary_min = Column(Integer, nullable=True)
    requested_salary_max = Column(Integer, nullable=True)
    salary_currency = Column(String, nullable=True)
    
    date_posted = Column(Date, nullable=True)
    status = Column(SQLAlchemyEnum(ApplicationStatusEnum), default=ApplicationStatusEnum.CONSIDERING, nullable=False)
    
    discovered_through_id = Column(Integer, ForeignKey("job_sources.id"), nullable=False)
    applied_through_text = Column(String, nullable=True) # Keep applied_through as a text field for now from schema
    referral = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="job_applications")
    discovered_via_source = relationship("JobSource", back_populates="job_applications")
    events = relationship("ApplicationEvent", back_populates="job_application", cascade="all, delete-orphan") 