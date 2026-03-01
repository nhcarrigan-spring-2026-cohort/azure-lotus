from fastapi import (
    APIRouter,
    Depends,
    Response,
    HTTPException
)

from sqlmodel import Session
from uuid import UUID
from core.database.session import get_session

from .models import Alert
from shared.api_response import ApiResponse

router=APIRouter()

@router.patch('/{alert_id}/resolve', response_model=ApiResponse)
async def resolve_alert(alert_id: UUID, response=Response, db: Session=Depends(get_session)):
    alert=db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(404, detail='Alert not found')
    
#    print(f'Alert obj: {alert}')
#    print(f'Resolved status: {alert.resolved}')

    alert.resolved=True
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return ApiResponse(success=True, message="", data=alert)