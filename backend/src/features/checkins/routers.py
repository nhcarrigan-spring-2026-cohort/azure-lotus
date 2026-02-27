from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.database.session import get_session
from features.checkins.models import CheckIn
from shared.api_response import ApiResponse
from shared.email_service import send_email_to_missing_checkin
from shared.filter_commands import CheckinFilterCommand, validate_checkin_filter_command

from .services import (
    create_daily_checkins_service,
    get_check_in_history,
    get_daily_checkin,
    get_missing_checkin_history,
    mark_missing_and_notify,
)

router = APIRouter()


def get_checkin_filter(
    offset: int = 0,
    limit: int = 10,
    from_date: date = None,
    to_date: date = None,
) -> CheckinFilterCommand:
    """Dependency to create CheckinFilterCommand from query parameters."""
    return CheckinFilterCommand(
        offset=offset, limit=limit, from_date=from_date, to_date=to_date
    )


@router.get("/{senior_id}/daily", response_model=ApiResponse)
async def senior_daily_checkin(
    senior_id: UUID,
    session: Session = Depends(get_session),
    payload: CheckinFilterCommand = Depends(get_checkin_filter),
):
    """Get the daily check-in of a senior."""
    if not validate_checkin_filter_command(payload):
        raise HTTPException(status_code=400, detail="Invalid filter command")

    daily_checkin = await get_daily_checkin(senior_id, session)
    return ApiResponse(success=True, message="", data=daily_checkin)


@router.get("/{senior_id}/history", response_model=ApiResponse)
async def senior_checkin_history(
    senior_id: UUID,
    session: Session = Depends(get_session),
    payload: CheckinFilterCommand = Depends(get_checkin_filter),
):
    """Get the history of check-ins for a senior."""
    if not validate_checkin_filter_command(payload):
        raise HTTPException(status_code=400, detail="Invalid filter command")

    checkin_history = await get_check_in_history(senior_id, payload, session)
    return ApiResponse(success=True, message="", data=checkin_history)


@router.get("/{senior_id}/missing", response_model=ApiResponse)
async def senior_missing_checkin_history(
    senior_id: UUID,
    session: Session = Depends(get_session),
    payload: CheckinFilterCommand = Depends(get_checkin_filter),
):
    """Get the missing history of check-ins for a senior."""
    if not validate_checkin_filter_command(payload):
        raise HTTPException(status_code=400, detail="Invalid filter command")

    missing_checkin_history = await get_missing_checkin_history(
        senior_id, payload, session
    )
    return ApiResponse(success=True, message="", data=missing_checkin_history)
