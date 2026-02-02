from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from src.shared.enums import InvitationStatus


class Invitation(SQLModel, table=True):
    __tablename__ = "invitations"

    id: int = Field(default=None, primary_key=True)

    senior_id: int = Field(foreign_key="senior_profiles.id")
    invited_by: int = Field(foreign_key="users.id")

    volunteer_email: str = Field(index=True)
    token: str = Field(index=True, unique=True)

    status: InvitationStatus = Field(default=InvitationStatus.PENDING)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    accepted_at: Optional[datetime] = None