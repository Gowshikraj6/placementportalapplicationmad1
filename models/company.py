from sqlalchemy import (
    Column, String, Integer, BigInteger, Text,
    ForeignKey, DateTime, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from config.db_creation import Base

class ApprovalStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class Company(Base):
    __tablename__ = "companies"

    id = Column(BigInteger, primary_key=True)
    company_name = Column(String(255), nullable=False, unique=True)

    hr_contact_name = Column(String(150))
    hr_contact_email = Column(String(150))
    hr_contact_phone = Column(String(20))

    website = Column(String(255))

    approval_status = Column(
        Enum(ApprovalStatus),
        default=ApprovalStatus.PENDING
    )

    description = Column(Text)
    industry = Column(String(150))
    headquarters = Column(String(200))

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationships
    placement_drives = relationship(
        "PlacementDrive",
        back_populates="company",
        cascade="all, delete-orphan"
    )