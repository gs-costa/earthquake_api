from datetime import datetime
from typing import Literal, TypeVar

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

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

    def get_by_date_range(
        self,
        date_column: str,
        start_time: datetime,
        end_time: datetime,
        order_by: str | None = None,
        order: Literal["asc", "desc"] = "desc",
        limit: int | None = None,
        **kwargs,
    ) -> list[BaseModel]:
        """
        Filter records by date range between start_time and end_time.

        Args:
            date_column: Name of the date/timestamp column to filter by
            start_time: Start datetime (inclusive)
            end_time: End datetime (inclusive)
            order_by: Column name to order by
            order: Sort order ('asc' or 'desc')
            limit: Maximum number of records to return
            **kwargs: Additional filters to apply

        Returns:
            List of records matching the criteria
        """
        try:
            query = self.session.query(self.model)

            date_column_attr = getattr(self.model, date_column)
            query = query.filter(date_column_attr >= start_time, date_column_attr <= end_time)

            if kwargs:
                query = query.filter_by(**kwargs)

            if order_by:
                query = query.order_by(text(f"{order_by} {order}"))

            if limit:
                query = query.limit(limit)

            results = query.all()
            self.logger.info(f"Found {len(results)} records between {start_time} and {end_time}")
            return list(results)

        except SQLAlchemyError as e:
            self.logger.error(f"Error filtering records by date range: {e}")
            raise e
