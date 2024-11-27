import uuid
from typing import Optional
from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db


class Allocation(db.Model):
    
    __tablename__ = "allocations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_name: Mapped[str] = mapped_column(String, nullable=False)
    student_id: Mapped[str] = mapped_column(ForeignKey("student_requests.student_id"), nullable=False)
    student_request: Mapped["StudentRequest"] = relationship("StudentRequest", back_populates="allocation")
    room_number: Mapped[str] = mapped_column(String, nullable=False)
    building_name: Mapped[str] = mapped_column(String(5), nullable=False)
    dormitory_id: Mapped[Optional[str]] = mapped_column(ForeignKey("dormitories.id"), nullable=True)
    dormitory: Mapped["Dormitory"] = relationship(back_populates="allocations")
    
    __table_args__ = (UniqueConstraint("student_id"),)