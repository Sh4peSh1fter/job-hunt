from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base
from .enums import JobSourceTypeEnum

class JobSource(Base):
    __tablename__ = "job_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    type = Column(SQLAlchemyEnum(JobSourceTypeEnum), nullable=True)
    website = Column(String, nullable=True)
    short_description = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    job_applications = relationship("JobApplication", back_populates="discovered_via_source") 