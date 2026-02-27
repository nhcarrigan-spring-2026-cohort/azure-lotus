from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    ValidationInfo,
    field_validator,
)
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    first_name: str
    last_name: str
    email: str = Field(index=True, unique=True)
    phone_number: str
    hashed_password: str

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class user_create(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr = Field(..., description="Unique email")
    phone_number: str
    password: str

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    # i didn't required role here we change it if it has to be here
    @field_validator("email", "first_name", "last_name", "phone_number", "password")
    @classmethod
    def not_empty(cls, v: str, info: ValidationInfo) -> str:
        if not v or v.strip() == "":
            field_name = info.field_name or "This field"
            raise ValueError(f"{field_name} is required and cannot be empty")
        return v

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


# here we can add like first_name and last_name or phone_number if it should be included
class login_request(SQLModel):
    email: EmailStr = Field(..., description="Unique email")
    password: str

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    @field_validator("email", "password")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError("This field is required and cannot be empty")
        return v

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class response(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str

    class Config:
        from_attributes = True
