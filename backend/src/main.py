from fastapi import FastAPI
from sqlmodel import SQLModel
from src.core.database.session import engine
from src.features.users.routers.auth import  auth_router
from src.core.setting import Settings
from src.core.middleware.jwt_auth import JWTAuthMiddleware
from sqlalchemy import text

app = FastAPI(title=Settings.APP_NAME)
app.include_router(auth_router, prefix="/auth", tags=["auth"])

app.add_middleware(JWTAuthMiddleware)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
def check_database():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "detail": str(e)}
