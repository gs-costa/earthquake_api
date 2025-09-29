import uuid

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, index=True, unique=True, default=uuid.uuid4)
