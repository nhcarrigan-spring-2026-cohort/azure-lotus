from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from core.database.session import get_session
from features.checkins.models import CheckIn
from shared.api_response import ApiResponse

from .services import (
    complete_checkin,
    create_todays_checkin,
    get_todays_checkin,
    trigger_alert,
)

router = APIRouter()


@router.post("", response_model=ApiResponse[CheckIn], status_code=201)
async def create_checkin(
    request: Request,
    session: Session = Depends(get_session),
):
    """Create today's check-in for the logged-in senior. Returns 400 if already exists today."""
    current_user_email = request.state.current_user["email"]
    checkin = await create_todays_checkin(current_user_email, session)
    return ApiResponse(success=True, message="Check-in created successfully", data=checkin)


@router.get("/today", response_model=ApiResponse[Optional[CheckIn]])
async def get_today_checkin(
    request: Request,
    session: Session = Depends(get_session),
):
    """Get today's check-in for the logged-in senior. Returns null if none exists."""
    current_user_email = request.state.current_user["email"]
    checkin = await get_todays_checkin(current_user_email, session)
    return ApiResponse(
        success=True,
        message="Today's check-in retrieved" if checkin else "No check-in for today",
        data=checkin,
    )


@router.put("/{checkin_id}/complete", response_model=ApiResponse[CheckIn])
async def complete_checkin_route(
    checkin_id: UUID,
    request: Request,
    session: Session = Depends(get_session),
):
    """Mark a check-in as complete. Records completed_at timestamp."""
    current_user_email = request.state.current_user["email"]
    checkin = await complete_checkin(checkin_id, current_user_email, session)
    return ApiResponse(success=True, message="Check-in marked as complete", data=checkin)


@router.put("/{checkin_id}/alert", response_model=ApiResponse[CheckIn])
async def alert_checkin(
    checkin_id: UUID,
    request: Request,
    session: Session = Depends(get_session),
):
    """Trigger an emergency alert. Sets status to ALERTED and notifies all caregivers."""
    current_user_email = request.state.current_user["email"]
    checkin = await trigger_alert(checkin_id, current_user_email, session)
    return ApiResponse(
        success=True,
        message="Emergency alert triggered for all caregivers",
        data=checkin,
    )
