from datetime import datetime, timezone
from typing import List

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel

from src.shared.enums import UserRole


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str = Field(index=True, unique=True)
    phone_number: str
    hashed_password: str

    roles: List[UserRole] = Field(
        default_factory=list,
        sa_column=Column(JSON),
    )

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
