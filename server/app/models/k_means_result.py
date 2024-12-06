import uuid
from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app import db


class KMeansResult(db.Model):
    
    __tablename__ = "k_means_results"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    result: Mapped[dict] = mapped_column(JSON, nullable=False)