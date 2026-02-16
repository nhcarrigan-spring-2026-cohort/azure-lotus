import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy import text
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.auth.auth import auth_router
from src.core.database.session import engine
from src.core.middleware.jwt_auth import JWTAuthMiddleware
from src.core.setting import Settings
from src.features.checkins.routers import router as check_in_router
from sqlalchemy import text
from core.setting import Settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=Settings.APP_NAME, version=Settings.VERSION)
app.add_middleware(JWTAuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins = Settings.BACKEND_CORS_ORIGINS,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(check_in_router, prefix="/check_in", tags=["checkin"])


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {"App Name":Settings.APP_NAME, "Version":Settings.VERSION, "message": "Hello World"}


@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "detail": str(e)}


@app.exception_handler(StarletteHTTPException)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"HTTP {exc.status_code} - {exc.detail} - Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers if exc.headers else None,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc_validation: RequestValidationError
):
    return JSONResponse(status_code=422, content={"detail": "validation error"})


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc_general: Exception):
    return JSONResponse(status_code=500, content={"detail": "internal server error"})
