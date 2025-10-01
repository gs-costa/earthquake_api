from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Double, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship

from src.app.database.models.base import BaseModel


class ExecutionLogs(BaseModel):
    __tablename__ = "execution_logs"

    id = Column(Integer, primary_key=True, index=True)  # type: ignore
    endpoint_name = Column(String, nullable=False, comment="Name of the endpoint being called.")
    execution_time = Column(Double, nullable=False, comment="Execution time in seconds.")
    status_code = Column(Integer, nullable=False, comment="Status code returned.")
    parameters = Column(JSON, nullable=True, comment="Parameters sent to the endpoint.")
    created_at = Column(DateTime, default=lambda: datetime.now(), comment="Creation time of the execution.")
    metadata_id = Column(PostgresUUID(as_uuid=True), ForeignKey("metadatas.id", ondelete="CASCADE"), nullable=False)

    metadatas = relationship("Metadatas", back_populates="execution_logs")
