from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel

class SeniorProfile(SQLModel, table=True):
    __tablename__ = "senior_profiles"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True)

    # NEW: Simple 1-on-1 assignment
    assigned_volunteer_id: Optional[int] = Field(default=None, foreign_key="users.id")

    emergency_contact_phone: str
    is_verified: bool = Field(default=False)
    medical_info: Optional[str] = None
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))