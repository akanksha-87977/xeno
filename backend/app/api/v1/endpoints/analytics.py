from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ....core.config import settings
from ....core.database import get_db
from ....services.analytics import AnalyticsService
from ....api.deps import get_current_active_user

router = APIRouter()

# In development we don't require auth for dashboard analytics
_auth_dep = get_current_active_user if settings.ENVIRONMENT != "development" else None


@router.get("/customers")
def get_customer_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(_auth_dep) if _auth_dep else None,
):
    """Get customer analytics"""
    return AnalyticsService.get_customer_analytics(db)


@router.get("/transactions")
def get_transaction_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(_auth_dep) if _auth_dep else None,
):
    """Get transaction analytics"""
    return AnalyticsService.get_transaction_analytics(db)


@router.get("/sql-insights")
def get_sql_insights(
    db: Session = Depends(get_db),
    current_user=Depends(_auth_dep) if _auth_dep else None,
):
    """Get SQL-based insights"""
    return AnalyticsService.get_sql_insights(db)
