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


router=APIRouter()

@router.get('/{alert_id}/resolve')
async def resolve_alert(alert_id: UUID, response=Response, db: Session=Depends(get_session)):
    alert=db.query(Alert).filter(Alert.id == alert_id).first()
#    print(f'Alert obj: {alert}')
    print(f'Resolved status: {alert.resolved}')
    return alert