from typing import Optional, Any
import jwt

from core.setting import Settings
from fastapi import APIRouter, Depends, HTTPException, Response, status, Cookie
from sqlmodel import Session
from starlette.responses import JSONResponse

from core.auth import security
from src.core.auth.security import hash_password, verify_password
from src.core.database.session import get_session
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


@auth_router.post('/refresh') 
async def refresh_token_route(res: Response, db: Session = Depends(get_session),
 refresh_token: Optional[str] = Cookie(None))-> Any:

    #Get the refresh token from cookie 
    if not refresh_token:
        return JSONResponse(
            status_code=401, 
            content={"detail": "Refresh token cookie missing...."}
        )    

    try:

        #  Decode the refresh token 
        jwt_decoded = jwt.decode(refresh_token, Settings.JWT_SECRET_KEY, algorithms=[Settings.ALGORITHM])
        payload = { 
                   "email":jwt_decoded.get('email'),
                   "user_id": jwt_decoded.get("user_id")
                   }

        new_refresh_token = security.create_refresh_token(payload)
        new_access_token = security.create_access_token(payload)

       
        user = db.query(User).filter(User.email == payload.get("email")).first()

        if not user:
          return JSONResponse(
            status_code=401,
            content={"detail": "User not found"}
            )

        # update refresh token 
        res.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=False,
            )

        return {
            "user_info": {
                "id":user.id,
                "email": user.email ,
                "phone_number": user.phone_number,
                "first_name": user.first_name,
                    },
          "access_token":new_access_token ,
        }

    except jwt.ExpiredSignatureError:
        return JSONResponse(status_code=401, content={"detail": "Refresh token expired. Please log in again."})
    except jwt.InvalidTokenError:
        return JSONResponse(status_code=401, content={"detail": "Invalid refresh token"})
    except Exception as e: 
        return JSONResponse(status_code=500, content={"detail": e})

