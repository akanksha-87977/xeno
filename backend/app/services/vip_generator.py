from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.customer import Customer, VIPCustomer

class VIPGeneratorService:
    
    VIP_CITIES = ['Delhi', 'Mumbai', 'Bangalore']
    DAYS_THRESHOLD = 60
    
    @staticmethod
    def generate_vip_customers(db: Session) -> int:
        """Generate VIP customers based on criteria"""
        
        # Calculate date threshold
        date_threshold = datetime.now().date() - timedelta(days=VIPGeneratorService.DAYS_THRESHOLD)
        
        # Query customers matching VIP criteria
        vip_candidates = db.query(Customer).filter(
            and_(
                Customer.city.in_(VIPGeneratorService.VIP_CITIES),
                Customer.signup_date >= date_threshold
            )
        ).all()
        
        # Clear existing VIP customers
        db.query(VIPCustomer).delete()
        
        # Insert new VIP customers
        count = 0
        for customer in vip_candidates:
            vip = VIPCustomer(
                customer_id=customer.customer_id,
                full_name=customer.full_name,
                email=customer.email,
                phone_number=customer.phone_number,
                city=customer.city,
                signup_date=customer.signup_date
            )
            db.add(vip)
            count += 1
        
        db.commit()
        return count
    
    @staticmethod
    def get_vip_customers(db: Session):
        """Get all VIP customers"""
        return db.query(VIPCustomer).all()
    
    @staticmethod
    def get_vip_stats(db: Session) -> dict:
        """Get VIP customer statistics"""
        vips = db.query(VIPCustomer).all()
        
        city_distribution = {}
        for vip in vips:
            city_distribution[vip.city] = city_distribution.get(vip.city, 0) + 1
        
        return {
            "total_vip_customers": len(vips),
            "city_distribution": city_distribution,
            "criteria": {
                "cities": VIPGeneratorService.VIP_CITIES,
                "days_threshold": VIPGeneratorService.DAYS_THRESHOLD
            }
        }