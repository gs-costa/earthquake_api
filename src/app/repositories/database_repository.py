from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.app.database.models.base import BaseModel
from src.logger import Logger


class DatabaseRepository:
    logger = Logger(__name__)

    def __init__(self, model: type[BaseModel], session: Session):
        self.model = model
        self.session = session

    def create(self, instance: BaseModel) -> BaseModel | None:
        try:
            self.session.add(instance)
            self.session.commit()
            self.session.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            self.session.rollback()
            self.logger.error(f"Error creating record: {instance}, error: {e}")
            raise e
