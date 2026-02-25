from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status
from pydantic import BaseModel, EmailStr
from sqlmodel import Session

from core.database.session import get_session
from shared.api_response import ApiResponse

from .services import create_relationship, delete_relationship, get_checkin_history, get_missing_checkins

router = APIRouter()


class CreateRelationshipRequest(BaseModel):
    email: EmailStr


@router.post(
    "",
    response_model=ApiResponse[dict],
    status_code=status.HTTP_201_CREATED,
)
async def add_relationship(
    body: CreateRelationshipRequest,
    request: Request,
    session: Session = Depends(get_session),
):
    """Create a relationship: the authenticated user becomes a caregiver for the
    user identified by the provided email (the senior).

    - 201 on success
    - 404 if email is not found
    - 409 if relationship already exists or self-monitoring attempted
    """
    current_user_email: str = request.state.current_user["email"]
    relationship = await create_relationship(
        current_user_email=current_user_email,
        target_email=body.email,
        session=session,
    )
    return ApiResponse(
        success=True,
        message="Relationship created",
        data={"id": str(relationship.id), "senior_id": str(relationship.senior_id)},
    )


@router.delete("/{relationship_id}", status_code=status.HTTP_200_OK)
async def remove_relationship(
    relationship_id: UUID,
    request: Request,
    session: Session = Depends(get_session),
):
    """Delete a relationship. Only the senior or caregiver in the relationship may do this.
    Check-in history is preserved.
    """
    current_user_email: str = request.state.current_user["email"]
    await delete_relationship(
        relationship_id=relationship_id,
        current_user_email=current_user_email,
        session=session,
    )
    return ApiResponse(success=True, message="Relationship deleted", data=None)


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


@router.get(
    "/{relationship_id}/checkins/missing",
    response_model=ApiResponse[list],
)
async def relationship_missing_checkins(
    relationship_id: UUID,
    request: Request,
    session: Session = Depends(get_session),
):
    """Get all missed check-ins for the senior in a relationship.

    A check-in counts as missed if its status is 'missed', or it is still 'pending'
    after the day it was scheduled (created_at date is before today).
    Results are ordered newest first.
    Only the senior or caregivers in the relationship may access this endpoint.
    """
    current_user_email: str = request.state.current_user["email"]
    missed = await get_missing_checkins(
        relationship_id=relationship_id,
        current_user_email=current_user_email,
        session=session,
    )
    return ApiResponse(success=True, message="Missed check-ins retrieved", data=missed)
