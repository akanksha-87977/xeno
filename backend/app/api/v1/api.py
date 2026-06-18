from fastapi import APIRouter

from .endpoints import auth, upload, customers, analytics, vip

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(upload.router, prefix="/upload", tags=["Upload"])
api_router.include_router(customers.router, prefix="/customers", tags=["Customers"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(vip.router, prefix="/vip", tags=["VIP Customers"])