from fastapi import FastAPI, HTTPException, Request, logger
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.openapi import custom_openapi
from core.setting import Settings
from shared.exceptions import *
from shared.scheduler import start_scheduler
from src.core.auth.auth import auth_router
from src.core.middleware.jwt_auth import JWTAuthMiddleware
from src.core.setting import Settings
from src.features.checkins.routers import router as check_in_router
from src.features.home.routers import router as home_router

app = FastAPI(title=Settings.APP_NAME, version=Settings.VERSION)

app.add_middleware(JWTAuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=Settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    start_scheduler()


app.openapi = custom_openapi(app)

app.include_router(home_router, tags=["home", "health-check"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(check_in_router, prefix="/check_in", tags=["checkin"])


app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
