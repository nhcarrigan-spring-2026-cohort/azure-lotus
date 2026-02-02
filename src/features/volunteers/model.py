from datetime import datetime

from sqlmodel import Field, SQLModel


class VolunteerProfile(SQLModel, table=True):
    __tablename__ = "volunteer_profiles"

    id: int  = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True)
    
    registered_at: datetime = Field(default_factory=datetime.utcnow)