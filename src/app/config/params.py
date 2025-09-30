from datetime import datetime

from fastapi import HTTPException, status


def validate_date_format(*args: str) -> None:
    """
    Validates the date format of the given arguments.
    Args:
        *args (str): The date strings to be validated.
    Raises:
        HTTPException: If the date format is invalid.
    """

    for data in args:
        if data:
            try:
                datetime.strptime(data, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid date format: Please enter the date in the correct format (yyyy-mm-dd)",
                )
