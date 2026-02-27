from datetime import date, datetime, timezone
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class CheckInCreate(SQLModel):
    senior_id: UUID = Field(foreign_key="users.id")
    status: str = Field(default="pending")


class CheckIn(SQLModel, table=True):
    __tablename__ = "checkins"
    __table_args__ = {"extend_existing": True}

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    senior_id: UUID = Field(foreign_key="users.id")
    status: str = Field(default="pending")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
