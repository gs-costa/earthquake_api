from sqlalchemy import TIMESTAMP, Column, Integer, String
from sqlalchemy.orm import relationship

from src.app.database.models.base import BaseModel


class Metadatas(BaseModel):
    __tablename__ = "metadatas"

    generated = Column(TIMESTAMP, nullable=False)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    api = Column(String, nullable=False)
    count = Column(Integer, nullable=False)

    features = relationship("Features", back_populates="metadatas")
    execution_logs = relationship("ExecutionLogs", back_populates="metadatas")
