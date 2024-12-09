from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from .. import db


class MaleStudentRequest(db.Model):
    
    __tablename__ = "male_student_requests"

    student_id: Mapped[str] = mapped_column(String(8), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    bedtime_habit: Mapped[str] = mapped_column(String, nullable=False)
    social_style: Mapped[str] = mapped_column(String, nullable=False)
    religion: Mapped[str] = mapped_column(String, nullable=False)
    academic_year: Mapped[int] = mapped_column(Integer, nullable=False)
    major: Mapped[str] = mapped_column(String, nullable=False)
    sports_passion: Mapped[str] = mapped_column(String, nullable=False)
    music_passion: Mapped[str] = mapped_column(String, nullable=False)
    gaming_passion: Mapped[str] = mapped_column(String, nullable=False)
    average_monthly_spending: Mapped[int] = mapped_column(Integer, nullable=False)
    is_smoker: Mapped[str] = mapped_column(String, nullable=False)
    
    
    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}