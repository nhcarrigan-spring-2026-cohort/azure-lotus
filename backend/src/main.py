import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from src.core.database.session import engine
from src.core.auth.auth import auth_router
from src.core.setting import Settings
from src.core.middleware.jwt_auth import JWTAuthMiddleware
from sqlalchemy import text

app = FastAPI(title=Settings.APP_NAME)
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.add_middleware(JWTAuthMiddleware)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

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


@app.exception_handler(StarletteHTTPException)
@app.exception_handler(HTTPException)  
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(
        f"HTTP {exc.status_code} - {exc.detail} - Path: {request.url.path}"
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers if exc.headers else None,
    )

