"""Reset password for allanbruno"""
from app.database import SessionLocal
from app.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()

user = db.query(User).filter(User.username == "allanbruno").first()
if user:
    user.password_hash = pwd_context.hash("senha123")
    db.commit()
    print(f"✅ Password reset for {user.username}")
else:
    print("❌ User not found")

db.close()