from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict, ValidationInfo 
from sqlalchemy import Column, Integer

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




class create_senior(BaseModel):
    assigned_volunteer_email: str
    emergency_contact_phone: str
    is_verified: bool 
    senior_email:str
    medical_info: Optional[str] 

    @field_validator('assigned_volunteer_email', 'emergency_contact_phone', 'medical_info') 
    @classmethod
    def not_empty(cls, v: str, info:ValidationInfo) -> str:
        if not v or v.strip() == "":
            field_name = info.field_name or "This field"
            raise ValueError(f"{field_name} is required and cannot be empty")
        return v


class senior_response(BaseModel):
    id: int
    user_id: int 
    assigned_volunteer_id:int 
    emergency_contact_phone: str
    is_verified: bool 
    medical_info: str

    class Config:
        from_attributes = True



