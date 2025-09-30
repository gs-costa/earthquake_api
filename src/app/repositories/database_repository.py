from typing import TypeVar

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.app.database.models.base import BaseModel
from src.logger import Logger

b_model = TypeVar("b_model", bound=BaseModel)


class DatabaseRepository:
    logger = Logger(__name__)

    def __init__(self, model: type[b_model], session: Session):
        self.model = model
        self.session = session

    def create(self, instance: b_model) -> b_model | None:
        try:
            self.session.add(instance)
            self.session.commit()
            self.session.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            self.session.rollback()
            self.logger.error(f"Error creating record: {instance}, error: {e}")
            raise e

    def bulk_create(self, instances: list[b_model]) -> list[b_model]:
        """Create multiple records in a single transaction for better performance."""
        try:
            self.session.add_all(instances)
            self.session.commit()

            for instance in instances:
                self.session.refresh(instance)
            self.logger.info(f"Successfully bulk created {len(instances)} records")
            return instances
        except SQLAlchemyError as e:
            self.session.rollback()
            self.logger.error(f"Error bulk creating records: {e}")
            raise e
