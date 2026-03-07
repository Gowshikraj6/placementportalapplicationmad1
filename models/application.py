from sqlalchemy import (
    Column, String, Integer, BigInteger, Text,
    ForeignKey, DateTime, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from config.db_creation import Base

class ApplicationStatus(enum.Enum):
    APPLIED = "APPLIED"
    SHORTLISTED = "SHORTLISTED"
    SELECTED = "SELECTED"
    REJECTED = "REJECTED"


class Application(Base):
    __tablename__ = "applications"

    id = Column(BigInteger, primary_key=True)

    student_id = Column(
        BigInteger,
        ForeignKey("student.id", ondelete="CASCADE"),
        nullable=False
    )

    drive_id = Column(
        BigInteger,
        ForeignKey("placement_drives.id", ondelete="CASCADE"),
        nullable=False
    )

    application_date = Column(DateTime, server_default=func.now())

    status = Column(
        Enum(ApplicationStatus),
        default=ApplicationStatus.APPLIED
    )

    notes = Column(Text)

    # Relationships
    student = relationship("Student")

    drive = relationship(
        "PlacementDrive",
        back_populates="applications"
    )