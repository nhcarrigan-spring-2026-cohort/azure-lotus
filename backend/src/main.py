import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy import text

# Your routers
from src.features.seniors.seniors import senior_router
from src.features.checkins.routers import router as check_in_router
from src.core.auth.auth import auth_router

# Database & settings
from src.core.database.session import engine
from src.core.setting import Settings

# Middleware
from src.core.middleware.jwt_auth import JWTAuthMiddleware
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
app.include_router(senior_router, tags=["seniors"])


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
