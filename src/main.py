from fastapi import FastAPI
from sqlmodel import SQLModel

from src.core.database.session import engine
from src.core.setting import Settings
from sqlalchemy import text

app = FastAPI(title=Settings.APP_NAME)

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
