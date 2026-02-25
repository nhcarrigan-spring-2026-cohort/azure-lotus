from typing import Optional

from fastapi import Request, status
from jwt import ExpiredSignatureError, PyJWTError, decode
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from src.core.setting import Settings


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        excluded_paths = {
            "/auth/login",
            "/auth/register",
            "/auth/refresh",
            "/auth/logout",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
        }

        if request.method == "OPTIONS" or request.url.path in excluded_paths:
            return await call_next(request)

        # Get Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Not authenticated - missing Authorization header"},
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Parse Bearer token
        scheme, _, token = auth_header.partition(" ")
        if scheme.lower() != "bearer" or not token.strip():
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authentication scheme or empty token"},
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            if not Settings.JWT_SECRET_KEY:
                return JSONResponse(
                    status_code=500,
                    content={
                        "detail": "Server configuration error: JWT secret key not set"
                    },
                )

            payload = decode(
                token,
                Settings.JWT_SECRET_KEY,
                algorithms=[Settings.ALGORITHM],
                options={"verify_signature": True, "require": ["exp", "iat"]},
            )

            email: Optional[str] = payload.get("email")
            if email is None:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Token malformed - missing email/user_id"},
                )

            request.state.current_user = {
                "email": email,
            }

        except ExpiredSignatureError:
            return JSONResponse(
                status_code=401, content={"detail": "Access token has expired"}
            )

        except PyJWTError as e:
            return JSONResponse(
                status_code=401, content={"detail": f"Invalid token: {str(e)}"}
            )

        response: Response = await call_next(request)
        return response
