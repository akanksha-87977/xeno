from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from datetime import datetime, timedelta
from typing import Dict, List
from ..models.customer import Customer, VIPCustomer
from ..models.transaction import Transaction, Order

class AnalyticsService:
    
    @staticmethod
    def get_customer_analytics(db: Session) -> Dict:
        # Fail fast to prevent frontend requests from hanging indefinitely.
        # Postgres-only; guard so analytics doesn't fail on other SQL engines.
        try:
            db.execute("SET statement_timeout = '5000ms'")
            db.execute("SET lock_timeout = '5000ms'")
        except Exception:
            pass

        """Get comprehensive customer analytics"""
        
        # NOTE: This endpoint is called on the frontend dashboard.
        # Keep each query bounded and avoid expensive/DB-specific calls
        # that can hang indefinitely (e.g. to_char with NULLs).

        total_customers = db.query(Customer).count()

        total_cities = db.query(func.count(func.distinct(Customer.city))).scalar() or 0

        gmail_count = (
            db.query(Customer).filter(Customer.is_gmail == True).count()
        )
        non_gmail_count = max(total_customers - gmail_count, 0)

        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        new_customers = (
            db.query(Customer)
            .filter(Customer.signup_date >= thirty_days_ago)
            .count()
        )

        customers_by_city = (
            db.query(Customer.city, func.count(Customer.id).label("count"))
            .group_by(Customer.city)
            .order_by(desc("count"))
            .limit(10)
            .all()
        )

        # Monthly signups (last 12 months)
        # Use DB-neutral month bucketing; if signup_date is NULL, ignore those rows.
        monthly_signups = (
            db.query(
                func.strftime("%Y-%m", Customer.signup_date).label("month"),
                func.count(Customer.id).label("count"),
            )
            .filter(Customer.signup_date.isnot(None))
            .group_by("month")
            .order_by("month")
            .limit(12)
            .all()
        )

        day_distribution = (
            db.query(Customer.signup_day, func.count(Customer.id).label("count"))
            .group_by(Customer.signup_day)
            .order_by(Customer.signup_day)
            .limit(7)
            .all()
        )
        
        
        return {
            "overview": {
                "total_customers": total_customers,
                "total_cities": total_cities,
                "gmail_customers": gmail_count,
                "non_gmail_customers": non_gmail_count,
                "new_customers_30_days": new_customers
            },
            "customers_by_city": [
                {"city": city, "count": count} for city, count in customers_by_city
            ],
            "monthly_signups": [
                {"month": month, "count": count} for month, count in monthly_signups
            ],
            "day_distribution": [
                {"day": day, "count": count} for day, count in day_distribution
            ],
            "gmail_distribution": {
                "gmail": gmail_count,
                "non_gmail": non_gmail_count
            }
        }
    
    @staticmethod
    def get_transaction_analytics(db: Session) -> Dict:
        # Fail fast to prevent frontend requests from hanging indefinitely.
        # Assumes Postgres.
        db.execute("SET statement_timeout = '5000ms'")
        db.execute("SET lock_timeout = '5000ms'")
        """Get transaction analytics"""
        
        # Total transactions
        total_transactions = db.query(Transaction).count()
        
        # Total revenue
        total_revenue = db.query(func.sum(Transaction.total_amount)).scalar() or 0
        
        # Average transaction amount
        avg_amount = db.query(func.avg(Transaction.total_amount)).scalar() or 0
        
        # Payment mode distribution
        payment_modes = db.query(
            Transaction.payment_mode,
            func.count(Transaction.id).label('count'),
            func.sum(Transaction.total_amount).label('total')
        ).group_by(Transaction.payment_mode).all()
        
        # Country-wise transactions
        country_stats = db.query(
            Transaction.country,
            func.count(Transaction.id).label('count'),
            func.sum(Transaction.total_amount).label('total')
        ).group_by(Transaction.country).all()
        
        # Daily transactions (last 30 days)
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        daily_transactions = db.query(
            Transaction.transaction_date,
            func.count(Transaction.id).label('count'),
            func.sum(Transaction.total_amount).label('total')
        ).filter(
            Transaction.transaction_date >= thirty_days_ago
        ).group_by(Transaction.transaction_date).order_by(Transaction.transaction_date).all()
        
        return {
            "overview": {
                "total_transactions": total_transactions,
                "total_revenue": round(total_revenue, 2),
                "average_amount": round(avg_amount, 2)
            },
            "payment_modes": [
                {
                    "mode": mode,
                    "count": count,
                    "total": round(total, 2)
                }
                for mode, count, total in payment_modes
            ],
            "country_stats": [
                {
                    "country": country,
                    "count": count,
                    "total": round(total, 2)
                }
                for country, count, total in country_stats
            ],
            "daily_transactions": [
                {
                    "date": str(date),
                    "count": count,
                    "total": round(total, 2)
                }
                for date, count, total in daily_transactions
            ]
        }
    
    @staticmethod
    def get_sql_insights(db: Session) -> List[Dict]:
        # Fail fast to prevent frontend requests from hanging indefinitely.
        # Assumes Postgres.
        db.execute("SET statement_timeout = '5000ms'")
        db.execute("SET lock_timeout = '5000ms'")
        """Execute predefined SQL analytics queries"""
        
        insights = []
        
        # 1. Customers from Delhi
        delhi_customers = db.query(Customer).filter(Customer.city == 'Delhi').limit(100).all()
        insights.append({
            "title": "Customers from Delhi",
            "query": "SELECT * FROM customers WHERE city = 'Delhi'",
            "result": [
                {
                    "customer_id": c.customer_id,
                    "full_name": c.full_name,
                    "email": c.email,
                    "city": c.city
                }
                for c in delhi_customers[:100]  # Limit to 100
            ],
            "count": len(delhi_customers)
        })
        
        # 2. Signups in last 30 days
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        recent_signups = (
            db.query(Customer)
            .filter(Customer.signup_date >= thirty_days_ago)
            .limit(100)
            .all()
        )
        insights.append({
            "title": "Signups in Last 30 Days",
            "query": f"SELECT * FROM customers WHERE signup_date >= '{thirty_days_ago}'",
            "result": [
                {
                    "customer_id": c.customer_id,
                    "full_name": c.full_name,
                    "email": c.email,
                    "signup_date": str(c.signup_date)
                }
                for c in recent_signups[:100]
            ],
            "count": len(recent_signups)
        })
        
        # 3. Unique cities count
        unique_cities = db.query(
            func.count(func.distinct(Customer.city))
        ).scalar()
        insights.append({
            "title": "Total Unique Cities",
            "query": "SELECT COUNT(DISTINCT city) FROM customers",
            "result": [{"unique_cities": unique_cities}],
            "count": unique_cities
        })
        
        # 4. Top 3 cities by signups
        top_cities = db.query(
            Customer.city,
            func.count(Customer.id).label('count')
        ).group_by(Customer.city).order_by(desc('count')).limit(3).all()
        insights.append({
            "title": "Top 3 Cities by Signups",
            "query": "SELECT city, COUNT(*) as count FROM customers GROUP BY city ORDER BY count DESC LIMIT 3",
            "result": [{"city": city, "count": count} for city, count in top_cities],
            "count": len(top_cities)
        })
        
        # 5. Customers without orders
        customers_without_orders = (
            db.query(Customer)
            .outerjoin(Order, Customer.customer_id == Order.customer_id)
            .filter(Order.id == None)
            .limit(100)
            .all()
        )
        insights.append({
            "title": "Customers Without Orders",
            "query": "SELECT c.* FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id WHERE o.id IS NULL",
            "result": [
                {
                    "customer_id": c.customer_id,
                    "full_name": c.full_name,
                    "email": c.email
                }
                for c in customers_without_orders[:100]
            ],
            "count": len(customers_without_orders)
        })
        
        # 6. Monthly signup count (bounded)
        monthly_count = (
            db.query(
                Customer.signup_month,
                func.count(Customer.id).label('count')
            )
            .group_by(Customer.signup_month)
            .order_by(Customer.signup_month)
            .limit(12)
            .all()
        )
        insights.append({
            "title": "Monthly Signup Count",
            "query": "SELECT signup_month, COUNT(*) as count FROM customers GROUP BY signup_month",
            "result": [{"month": month, "count": count} for month, count in monthly_count],
            "count": len(monthly_count)
        })
        
        # 7. Cities with more than 20 customers (bounded)
        cities_20_plus = (
            db.query(
                Customer.city,
                func.count(Customer.id).label('count')
            )
            .group_by(Customer.city)
            .having(func.count(Customer.id) > 20)
            .order_by(desc('count'))
            .limit(10)
            .all()
        )
        insights.append({
            "title": "Cities with More Than 20 Customers",
            "query": "SELECT city, COUNT(*) as count FROM customers GROUP BY city HAVING COUNT(*) > 20",
            "result": [{"city": city, "count": count} for city, count in cities_20_plus],
            "count": len(cities_20_plus)
        })

        
        # 8. Date with highest signups
        max_signup_date = db.query(
            Customer.signup_date,
            func.count(Customer.id).label('count')
        ).group_by(Customer.signup_date).order_by(desc('count')).first()
        if max_signup_date:
            insights.append({
                "title": "Date with Highest Signups",
                "query": "SELECT signup_date, COUNT(*) as count FROM customers GROUP BY signup_date ORDER BY count DESC LIMIT 1",
                "result": [{"date": str(max_signup_date[0]), "count": max_signup_date[1]}],
                "count": 1
            })
        
        # 9. Day with highest signups
        max_signup_day = db.query(
            Customer.signup_day,
            func.count(Customer.id).label('count')
        ).group_by(Customer.signup_day).order_by(desc('count')).first()
        if max_signup_day:
            insights.append({
                "title": "Day with Highest Signups",
                "query": "SELECT signup_day, COUNT(*) as count FROM customers GROUP BY signup_day ORDER BY count DESC LIMIT 1",
                "result": [{"day": max_signup_day[0], "count": max_signup_day[1]}],
                "count": 1
            })
        
        return insights