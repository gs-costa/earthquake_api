from sqlalchemy import DECIMAL, TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship

from src.app.database.models.base import BaseModel


class Features(BaseModel):
    __tablename__ = "features"

    mag = Column(DECIMAL, nullable=True)
    place = Column(String, nullable=True)
    time = Column(TIMESTAMP, nullable=True)
    updated = Column(TIMESTAMP, nullable=True)
    tz = Column(Integer, nullable=True)
    url = Column(String, nullable=True)
    detail = Column(String, nullable=True)
    felt = Column(Integer, nullable=True)
    cdi = Column(DECIMAL, nullable=True)
    mmi = Column(DECIMAL, nullable=True)
    alert = Column(String, nullable=True)
    status = Column(String, nullable=True)
    tsunami = Column(Integer, nullable=True)
    sig = Column(Integer, nullable=True)
    net = Column(String, nullable=True)
    code = Column(String, nullable=True)
    ids = Column(String, nullable=True)
    sources = Column(String, nullable=True)
    types = Column(String, nullable=True)
    nst = Column(Integer, nullable=True)
    dmin = Column(DECIMAL, nullable=True)
    rms = Column(DECIMAL, nullable=True)
    gap = Column(DECIMAL, nullable=True)
    mag_type = Column(String, nullable=True)

    latitude = Column(DECIMAL, nullable=True)
    longitude = Column(DECIMAL, nullable=True)
    depth = Column(DECIMAL, nullable=True)
    event_id = Column(String, nullable=False)
    metadata_id = Column(PostgresUUID(as_uuid=True), ForeignKey("metadatas.id", ondelete="CASCADE"), nullable=False)

    metadatas = relationship("Metadatas", back_populates="features")
