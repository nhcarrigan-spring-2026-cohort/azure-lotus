from datetime import time
from sqlalchemy import func
from jwt import decode
from fastapi import APIRouter, Depends, Response, HTTPException, Request
from sqlmodel import Session
from src.features.seniors.models import SeniorProfile, create_senior, senior_response
from src.features.users.models import User
from src.core.database.session import get_session
from src.core.setting import Settings
from sqlalchemy.orm.exc import NoResultFound

senior_router = APIRouter()

@senior_router.post("/senior", response_model=senior_response)
def create_senior_endpoint(senior: create_senior, request: Request, db: Session = Depends(get_session)):
    try:

        # 1️⃣ Extract JWT from header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Missing token")
        token = auth_header.split(" ")[1]

        if not Settings.JWT_SECRET_KEY:
            raise HTTPException(500, detail="JWT_SECRET_KEY not found")

        payload = decode(
            token,
            Settings.JWT_SECRET_KEY,
            algorithms=[Settings.ALGORITHM],
            options={"verify_signature": True, "require": ["exp", "iat"]},
        )

        email = payload.get("email")
        if not email:
            raise HTTPException(401, detail="Malformed JWT")

        # Ensure the creator is a family user
        try:
            family_user = db.query(User).filter(User.email == email).one()
            print("first", family_user.roles)
            if "family" not in family_user.roles:
                 raise HTTPException(
                    status_code=403,
                    detail="Only users with family role can create senior profiles"
                )
                 
        except NoResultFound:
            raise HTTPException(401, detail="Family user not found")

        #Check if assigned volunteer exists and is actually a volunteer
        try:
            assigned_volunteer = db.query(User).filter(User.email == senior.assigned_volunteer_email).one() 
            print("second",assigned_volunteer.roles)
            if  "volunteer" not in assigned_volunteer.roles:
                 raise HTTPException(
                    status_code=403,
                    detail="Assigned user is not a volunteer"
                )
                 

        except NoResultFound:
            raise HTTPException(404, detail="Assigned volunteer not found or not a volunteer")

        #Check if the senior user exists
        try:
            senior_user = db.query(User).filter(User.email == senior.senior_email).one()
            if  "senior" not in senior_user.roles: 
                raise HTTPException(
                    status_code=403,
                    detail="User is not a senior"
                )

        except NoResultFound:
            raise HTTPException(404, detail="Senior user not found")


        #Ensure senior profile does not already exist
        existing_profile = db.query(SeniorProfile).filter(SeniorProfile.user_id == senior_user.id).first()
        if existing_profile:
            raise HTTPException(400, detail="Senior profile already exists")


        new_profile = SeniorProfile(
            user_id=senior_user.id,
            assigned_volunteer_id=assigned_volunteer.id,
            emergency_contact_phone=senior.emergency_contact_phone,
            is_verified=senior.is_verified,
            medical_info=senior.medical_info
        )

        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)

        return new_profile

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

