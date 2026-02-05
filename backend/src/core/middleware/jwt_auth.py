from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from jwt import decode, ExpiredSignatureError, PyJWTError  
from features.users.utils import JWT_SECRET_KEY  
from typing import Optional

ALGORITHM = "HS256"
class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        excluded_paths = {
            "/auth/login",
            "/auth/register",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
            # "/", based on our need we can uncomment these
            # "/auth/refresh",   
        }

        if request.method == "OPTIONS" or request.url.path in excluded_paths:
            return await call_next(request)

        # Get Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated - missing Authorization header",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Parse Bearer token
        scheme, _, token = auth_header.partition(" ")
        if scheme.lower() != "bearer" or not token.strip():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme or empty token",
                headers={"WWW-Authenticate": "Bearer"},
            )


        try:
            if not JWT_SECRET_KEY:
                raise HTTPException(
                    status_code=500,
                    detail="Server configuration error: JWT secret key not set"
                )

            payload = decode(
                token,
                JWT_SECRET_KEY,
                algorithms=[ALGORITHM],
                options={"verify_signature": True, "require": ["exp", "iat"]},  
            )

            email: Optional[str] = payload.get("email") # or we can use user id here  
            if email is None:
                raise HTTPException(status_code=401, detail="Token malformed - missing email/user_id")

            request.state.current_user = {"email": email, "roles": payload.get("roles", [])}

        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Access token has expired")
        except PyJWTError as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

        response: Response = await call_next(request)
        return response
