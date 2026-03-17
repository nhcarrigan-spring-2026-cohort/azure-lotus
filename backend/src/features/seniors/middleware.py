from jwt import decode
from src.core.setting import Settings
from core.database.session import get_session
from core.middleware import jwt_auth
from fastapi import Request, status, HTTPException,Depends
from sqlmodel import Session 

# get the user info mean the from jwt decode it and get the email check if user exist and if the role is family 
# check if the family exist in the db and also check if the person is has roe family
async def senior_check(request:Request, db: Session = Depends(get_session)):
    if request.url.path.starwith("/senior"):
        pass

