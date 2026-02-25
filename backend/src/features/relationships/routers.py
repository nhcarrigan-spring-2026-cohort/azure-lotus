from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request
from sqlmodel import Session

from core.database.session import get_session
from features.checkins.models import CheckIn
from shared.api_response import ApiResponse

from .services import get_checkin_history

router = APIRouter()


@router.get(
    "/{relationship_id}/checkins/history",
    response_model=ApiResponse[dict],
)
async def relationship_checkin_history(
    relationship_id: UUID,
    request: Request,
    session: Session = Depends(get_session),
    page: int = Query(default=1, ge=1, description="Page number (1-based)"),
    limit: int = Query(default=10, ge=1, le=100, description="Items per page"),
):
    """Get paginated check-in history for the senior in a relationship.

    Only the senior or caregivers that are part of the relationship may access this endpoint.
    Results are sorted by most recent check-in first.
    """
    current_user_email: str = request.state.current_user["email"]
    data = await get_checkin_history(
        relationship_id=relationship_id,
        current_user_email=current_user_email,
        session=session,
        page=page,
        limit=limit,
    )
    return ApiResponse(success=True, message="Check-in history retrieved", data=data)
