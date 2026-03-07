from flask_security import UserMixin
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from config.db_creation import Base
from datetime import datetime

class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(255), unique=True)

    password = Column(String(255), nullable=False)

    active = Column(Boolean(), default=True)
    is_approved = Column(Boolean, default=False)

    # 🔹 auditing fields
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, nullable=True)

    approved_at = Column(DateTime, nullable=True)
    approved_by = Column(Integer, nullable=True)

    roles = relationship(
        "Role",
        secondary=roles_users,
        backref="users"
    )