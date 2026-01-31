"""
User Seeder - Seeds demo user into the database
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.base import SessionLocal, engine
from app.models.user import User
from app.core.security import get_password_hash


def seed_demo_user():
    """Create demo user if not exists."""
    db: Session = SessionLocal()
    
    try:
        # Check if demo user already exists
        existing_user = db.query(User).filter(User.email == "demo@petiksendiri.com").first()
        
        if existing_user:
            print("Demo user already exists. Skipping...")
            return
        
        # Create demo user
        demo_user = User(
            email="demo@petiksendiri.com",
            username="demo",
            hashed_password=get_password_hash("demo123"),
            full_name="Demo User",
            is_active=True,
            is_superuser=True
        )
        
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)
        
        print("=" * 50)
        print("Demo user created successfully!")
        print("=" * 50)
        print(f"Email: demo@petiksendiri.com")
        print(f"Username: demo")
        print(f"Password: demo123")
        print(f"Full Name: Demo User")
        print(f"Is Superuser: True")
        print("=" * 50)
        
    except Exception as e:
        print(f"Error seeding demo user: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Starting user seeder...")
    seed_demo_user()
    print("Seeding completed!")
