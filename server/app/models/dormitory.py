import uuid
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app import db


class Dormitory(db.Model):
    
    __tablename__ = "dormitories"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    building_name: Mapped[str] = mapped_column(String, nullable=False)
    total_rooms: Mapped[int] = mapped_column(Integer, nullable=False)
    students_per_room: Mapped[int] = mapped_column(Integer, nullable=False)
    
    
    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}