from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from core.database.session import get_session
from shared.api_response import ApiResponse

from .services import get_alerts_for_user, resolve_alert

router = APIRouter()


@router.get("", response_model=ApiResponse[list])
async def get_alerts(
    request: Request,
    session: Session = Depends(get_session),
):
    """Get all unresolved alerts for the logged-in user's seniors."""
    current_user_email: str = request.state.current_user["email"]
    alerts = await get_alerts_for_user(current_user_email, session)
    return ApiResponse(success=True, message="Alerts retrieved", data=alerts)


@router.put("/{alert_id}/resolve", response_model=ApiResponse[dict])
async def resolve_alert_route(
    alert_id: UUID,
    request: Request,
    session: Session = Depends(get_session),
):
    """Mark an alert as resolved."""
    current_user_email: str = request.state.current_user["email"]
    alert = await resolve_alert(alert_id, current_user_email, session)
    return ApiResponse(success=True, message="Alert resolved", data={"id": str(alert.id), "resolved": alert.resolved})
