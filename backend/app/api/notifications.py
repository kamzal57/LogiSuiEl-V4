from fastapi import APIRouter, Depends

from ..dependencies import get_current_admin
from ..models import User
from ..schemas import ReportResponse

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/test", response_model=dict)
async def send_test_notification(
    _: User = Depends(get_current_admin),
) -> dict:
    # Placeholder endpoint for future integrations (SMS, email, etc.)
    return {"status": "ok", "message": "Notification envoyée (simulation)"}
