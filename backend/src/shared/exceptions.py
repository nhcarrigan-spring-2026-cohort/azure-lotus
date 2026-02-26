from fastapi import Request, HTTPException, logger
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"HTTP {exc.status_code} - {exc.detail} - Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers if exc.headers else None,
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(status_code=422, content={"detail": "validation error"})


async def general_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error occurred")
    return JSONResponse(status_code=500, content={"detail": "internal server error"})