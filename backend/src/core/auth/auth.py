from typing import Any

import jwt
from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from sqlmodel import Session
from starlette.responses import JSONResponse

from core.auth import security
from src.core.auth.security import create_access_token, hash_password, verify_password
from src.core.database.session import get_session
from src.core.setting import Settings
from src.features.users.models import User, login_request, response, user_create

auth_router = APIRouter()


@auth_router.post("/register", response_model=response, status_code=201)
def Register(
    user: user_create, response: Response, db: Session = Depends(get_session)
) -> Any:
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
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@auth_router.post("/login")
def login(
    user: login_request, response: Response, db: Session = Depends(get_session)
) -> Any:
    existing_user = db.query(User).filter(User.email == user.email).first()

    if not existing_user or not verify_password(
        user.password, existing_user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    # Create token
    payload = {"user_id": str(existing_user.id), "email": str(existing_user.email)}
    token = security.create_token_pair(payload)

    # Set token as cookie
    response.set_cookie(
        key="refresh_token",
        value=token.get("refresh_token"),
        httponly=True,
        secure=False,
    )

    # Return user info
    return {
        "user_info": {
            "id": existing_user.id,
            "email": existing_user.email,
            "phone_number": existing_user.phone_number,
            "first_name": existing_user.first_name,
            "access_token": token.get("access_token"),
        }
    }


@auth_router.post("/logout", status_code=status.HTTP_200_OK)
def logout(response: Response):
    """Invalidate the session by clearing the refresh token cookie."""
    response.delete_cookie(key="refresh_token", httponly=True)
    return {"message": "Logged out successfully"}


@auth_router.post("/refresh", status_code=status.HTTP_200_OK)
def refresh(
    response: Response,
    db: Session = Depends(get_session),
    refresh_token: str = Cookie(default=None),
):
    """Issue a new access token using the refresh token stored in the cookie."""
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token provided",
        )

    if not Settings.JWT_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Server configuration error")

    try:
        payload = jwt.decode(
            refresh_token,
            Settings.JWT_SECRET_KEY,
            algorithms=[Settings.ALGORITHM],
            options={"verify_signature": True, "require": ["exp", "iat"]},
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    email = payload.get("email")
    user_id = payload.get("user_id")
    if not email or not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload malformed",
        )

    new_access_token = create_access_token({"user_id": user_id, "email": email})
    return {"access_token": new_access_token, "token_type": "bearer"}
