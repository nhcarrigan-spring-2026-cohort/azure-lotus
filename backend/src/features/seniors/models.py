from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel

class SeniorProfile(SQLModel, table=True):
    __tablename__ = "senior_profiles"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Links directly to the User table
    # REMOVED "nullable=False" because "user_id: int" already handles that
    user_id: int = Field(
        foreign_key="users.id",
        unique=True,
    )

    phone_number: str
    emergency_contact_phone: str
    check_in_deadline: str = Field(default="10:00")
    is_verified: bool = Field(default=False)
    medical_info: Optional[str] = None
    
    # Added for consistency with User model
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SeniorVolunteer(SQLModel, table=True):
    __tablename__ = "senior_volunteers"

    id: Optional[int] = Field(default=None, primary_key=True)

    senior_id: int = Field(foreign_key="senior_profiles.id")
    volunteer_id: int = Field(foreign_key="users.id")

    active: bool = Field(default=True)
    
    # Added so you know WHEN they started volunteering
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))