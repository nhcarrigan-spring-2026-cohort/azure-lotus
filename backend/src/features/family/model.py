from sqlmodel import Field, SQLModel


class FamilyProfile(SQLModel, table=True):
    __tablename__ = "family_profiles"

    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True)