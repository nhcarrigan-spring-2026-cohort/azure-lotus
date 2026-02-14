from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel

from src.shared.enums import CheckInMethod, CheckInStatus


class CheckInBase(SQLModel):
    # "The Ticket": Created automatically at midnight (or manually)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Defaults to PENDING so the system knows to watch it
    status: CheckInStatus = Field(default=CheckInStatus.PENDING)
    
    method: CheckInMethod = Field(default=CheckInMethod.SYSTEM)

class CheckInCreate(SQLModel):
    senior_id: int = Field(foreign_key="senior_profiles.id")
    
    # The specific deadline for THIS day (e.g., "Feb 3rd at 10:00 AM")
    check_in_deadline: datetime    

class CheckIn(SQLModel, table=True):
    __tablename__ = "checkins"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
