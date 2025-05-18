from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base
from .enums import ApplicationEventTypeEnum

class ApplicationEvent(Base):
    __tablename__ = "application_events"

    id = Column(Integer, primary_key=True, index=True)
    job_application_id = Column(Integer, ForeignKey("job_applications.id"), nullable=False)
    
    event_type = Column(SQLAlchemyEnum(ApplicationEventTypeEnum), nullable=False)
    event_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    participants = Column(Text, nullable=True) # Changed from required to nullable as per typical usage
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    job_application = relationship("JobApplication", back_populates="events") 