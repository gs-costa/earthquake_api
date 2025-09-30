import logging


class Logger:
    """Logger class for application logging."""

    def __init__(self, name: str | None = None, level: int = logging.INFO):
        """Initialize the logger.

        Args:
            name: Logger name, defaults to module name
            level: Logging level, defaults to DEBUG
        """
        self.logger = logging.getLogger(name or __name__)
        self.logger.setLevel(level)

        parent_has_handlers = bool(self.logger.parent and self.logger.parent.handlers)
        if not self.logger.handlers and not parent_has_handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def debug(self, msg: str) -> None:
        """Log debug message."""
        self.logger.debug(msg)

    def info(self, msg: str) -> None:
        """Log info message."""
        self.logger.info(msg)

    def warning(self, msg: str) -> None:
        """Log warning message."""
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        """Log error message."""
        self.logger.error(msg)

    def critical(self, msg: str) -> None:
        """Log critical message."""
        self.logger.critical(msg)
