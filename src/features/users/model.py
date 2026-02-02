from datetime import datetime

from sqlmodel import Field, SQLModel

from src.shared.enums import UserRole


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int  = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str = Field(index=True, unique=True)
    password: str
    role: UserRole

    created_at: datetime = Field(default_factory=datetime.utcnow)