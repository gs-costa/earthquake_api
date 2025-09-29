from sqlalchemy import Column, Integer, String

from src.app.database.models.base import BaseModel


class Metadata(BaseModel):
    __tablename__ = "metadata"

    generated = Column(Integer, nullable=False)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    api = Column(String, nullable=False)
    count = Column(Integer, nullable=False)
