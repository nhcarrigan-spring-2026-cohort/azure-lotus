from typing import List, Optional, Any
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from src.core.database.session import get_session
from src.features.alerts.models import Alert 

alert_router = APIRouter()

@alert_router.get("/alerts")
def get_alerts(
    resolved: Optional[bool] = Query(None, description="Filter: ?resolved=false for active issues"),
    db: Session = Depends(get_session)
) -> Any:

    try:
        statement = select(Alert)
        
        if resolved is not None:
            statement = statement.where(Alert.resolved == resolved)
        
        results = db.exec(statement).all()
        
        return results

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Internal Server Error: {str(e)}"}
        )
