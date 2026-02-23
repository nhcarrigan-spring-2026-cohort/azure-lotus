from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Relationship(SQLModel, table=True):
    __tablename__ = "relationships"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    senior_id: UUID = Field(foreign_key="users.id")
    caregiver_id: UUID = Field(foreign_key="users.id")
    priority: int = Field(default=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
