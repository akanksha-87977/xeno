from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ....core.database import get_db
from ....models.user import User
from ....schemas.customer import VIPCustomer
from ....services.vip_generator import VIPGeneratorService
from ....api.deps import get_current_active_user

router = APIRouter()

@router.post("/generate")
def generate_vip_customers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Generate VIP customers based on criteria"""
    
    count = VIPGeneratorService.generate_vip_customers(db)
    
    return {
        "message": f"Generated {count} VIP customers",
        "count": count
    }

@router.get("/", response_model=List[VIPCustomer])
def get_vip_customers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all VIP customers"""
    return VIPGeneratorService.get_vip_customers(db)

@router.get("/stats")
def get_vip_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get VIP customer statistics"""
    return VIPGeneratorService.get_vip_stats(db)