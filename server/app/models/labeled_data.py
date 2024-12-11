import uuid
from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app import db


class LabledData(db.Model):
    
    __tablename__ = "labeled_data"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    json: Mapped[dict] = mapped_column(JSON, nullable=False)
    
    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}