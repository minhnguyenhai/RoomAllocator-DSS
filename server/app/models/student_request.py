from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db


class StudentRequest(db.Model):
    
    __tablename__ = "student_requests"

    student_id: Mapped[str] = mapped_column(String(8), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    gender: Mapped[str] = mapped_column(String(6), nullable=False)
    rent_per_month: Mapped[int] = mapped_column(Integer, nullable=False)
    people_per_room: Mapped[int] = mapped_column(Integer, nullable=False)
    private_toilet: Mapped[int] = mapped_column(Integer, nullable=False)
    water_heater: Mapped[int] = mapped_column(Integer, nullable=False)
    air_conditioner: Mapped[int] = mapped_column(Integer, nullable=False)
    primary_study_time: Mapped[str] = mapped_column(String, nullable=False)
    social_style: Mapped[str] = mapped_column(String, nullable=False)
    silent_space_required: Mapped[bool] = mapped_column(Boolean, nullable=False)
    bed_time_habit: Mapped[str] = mapped_column(String, nullable=False)
    is_smoker: Mapped[bool] = mapped_column(Boolean, nullable=False)
    allocation: Mapped["Allocation"] = relationship("Allocation", back_populates="student_request", uselist=False)