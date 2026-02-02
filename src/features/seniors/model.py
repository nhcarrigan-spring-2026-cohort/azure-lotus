from typing import Optional

from sqlmodel import Field, SQLModel


class SeniorProfile(SQLModel, table=True):
    __tablename__ = "senior_profiles"

    id: int  = Field(default=None, primary_key=True)

    # Senior MAY be a user (for self check-in)
    user_id: int = Field(
        default=None,
        foreign_key="users.id",
        unique=True
    )

    family_id: int = Field(foreign_key="family_profiles.id")

    name: str
    medical_info: Optional[str] = None
    emergency_contact: str
    


class SeniorVolunteer(SQLModel, table=True):
    __tablename__ = "senior_volunteers"

    id: int = Field(default=None, primary_key=True)

    senior_id: int = Field(foreign_key="senior_profiles.id")
    volunteer_id: int = Field(foreign_key="volunteer_profiles.id")

    active: bool = Field(default=True)