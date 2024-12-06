from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app import db


class StudentRequest(db.Model):
    
    __tablename__ = "student_requests"

    student_id: Mapped[str] = mapped_column(String(8), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    gender: Mapped[str] = mapped_column(String(5), nullable=False)
    bedtime_habit: Mapped[str] = mapped_column(String, nullable=False)
    social_style: Mapped[str] = mapped_column(String, nullable=False)
    religion: Mapped[str] = mapped_column(String, nullable=False)
    academic_year: Mapped[int] = mapped_column(Integer, nullable=False)
    major: Mapped[str] = mapped_column(String, nullable=False)
    sports_passion_score: Mapped[int] = mapped_column(Integer, nullable=False)
    music_passion_score: Mapped[int] = mapped_column(Integer, nullable=False)
    gaming_passion_score: Mapped[int] = mapped_column(Integer, nullable=False)
    average_monthly_spending: Mapped[int] = mapped_column(Integer, nullable=False)
    
    
    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}