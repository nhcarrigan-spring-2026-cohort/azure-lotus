from core.auth import security
from fastapi import APIRouter, Depends, Response,HTTPException, status, Response
from starlette.responses import JSONResponse 
from src.core.auth.security import hash_password,verify_password
auth_router = APIRouter()
from src.features.users.models import User, user_create, response, login_request
from src.core.database.session import get_session
from sqlmodel import Session 
from typing import Any
from src.core.setting import *



@auth_router.post("/register",response_model=response)
def Register(user: user_create,  response:Response, db: Session = Depends(get_session) ) -> Any:
  try:
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

  except Exception as e: 
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)}
        )


@auth_router.post("/login")
def login(user: login_request, response: Response, db: Session = Depends(get_session)) -> Any:
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()

        if not existing_user or not verify_password(user.password, existing_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        # Create token
        payload = {"user_id": str(existing_user.id), "email": str(existing_user.email)}
        token = security.create_token_pair(payload)

        # Set token as cookie
        response.set_cookie(key="refresh_token", value=token.get("refresh_token"), httponly=True, secure=False)

        # Return user info 
        return {
        "user_info": {
            "id": existing_user.id,
            "email": existing_user.email,
            "phone_number": existing_user.phone_number,
            "first_name": existing_user.first_name,
            "access_token": token.get("access_token")
        }
    }   

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail":str(e)}
        )

