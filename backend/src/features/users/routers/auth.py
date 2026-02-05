from fastapi import APIRouter, Depends, HTTPException, status
from features.users import utils
from src.features.users.utils import hash_password,verify_password
auth_router = APIRouter()
from src.features.users.schemas.user_create import user_create, response, login_equest
from src.core.database.session import get_session
from sqlmodel import Session 
from typing import Any
from src.features.users.models import User
from src.features.users.utils import *

@auth_router.post("/register",response_model=response)
def Register(user: user_create, db: Session = Depends(get_session)) -> Any:
     existing = db.query(User).filter(User.email == user.email).first()
     if existing:
        raise HTTPException(400, detail="Email already registered")
     
     hashed_password = hash_password(user.password)
     new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone_number=user.phone_number,
        hashed_password=hashed_password,
        roles=user.roles,
    ) 
    
     db.add(new_user)
     db.commit()
     db.refresh(new_user)

     return new_user


@auth_router.post("/login") 
def Login(user: login_equest, db: Session = Depends(get_session)) -> Any:
        existing_user = db.query(User).filter(User.email == user.email).first()

        if not existing_user or not verify_password(user.password, existing_user.hashed_password):
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
            )
        payload = {"user_id": str(existing_user.id), "email":str(existing_user.email)}
        token = utils.create_token_pair(payload)

        return {
        "user_info": {
            "id": existing_user.id,
            "email": existing_user.email,
            "phone_number": existing_user.phone_number,
            "first_name": existing_user.first_name,          
        },
        "tokens": token,
    }


