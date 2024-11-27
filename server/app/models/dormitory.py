import uuid
from typing import List
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db


class Dormitory(db.Model):
    
    __tablename__ = "dormitories"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    building_name: Mapped[str] = mapped_column(String(5), unique=True, nullable=False)
    total_floors: Mapped[int] = mapped_column(Integer, nullable=False)
    rooms_per_floor: Mapped[int] = mapped_column(Integer, nullable=False)
    rent_per_month: Mapped[int] = mapped_column(Integer, nullable=False)
    people_per_room: Mapped[int] = mapped_column(Integer, nullable=False)
    private_toilet: Mapped[int] = mapped_column(Integer, nullable=False)
    water_heater: Mapped[int] = mapped_column(Integer, nullable=False)
    air_conditioner: Mapped[int] = mapped_column(Integer, nullable=False)
    allocations: Mapped[List["Allocation"]] = relationship(back_populates="dormitory")