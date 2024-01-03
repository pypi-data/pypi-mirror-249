import logging
import json
from datetime import datetime
from logging import LoggerAdapter


class CustomJsonFormatter(logging.Formatter):
    """
    A custom log formatter that formats log records as JSON objects.

    This formatter converts log records into JSON format, including
    information such as the timestamp, log level, message, filename,
    line number, function name, user UUID, and correlation ID.

    Attributes:
        None

    Methods:
        format(record): Formats the log record as a JSON object.

    Usage:
        To use this formatter, create an instance of CustomJsonFormatter
        and set it as the formatter for a logging handler.
    """

    def format(self, record):
        log_object = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "filename": record.filename,
            "lineno": record.lineno,
            "funcName": record.funcName,
            "userUUID": getattr(record, "userUUID", ""),
            "correlationID": getattr(record, "correlationID", ""),
        }
        return json.dumps(log_object)


class CustomLoggerAdapter(LoggerAdapter):
    """
    A custom logger adapter that adds additional context to log messages.

    This logger adapter extends the functionality of the standard logger
    by adding user UUID and correlation ID to log messages.

    Attributes:
        None

    Methods:
        process(msg, kwargs): Adds additional context to the log message.

    Usage:
        To use this logger adapter, create an instance of CustomLoggerAdapter
        and pass it a logger and a dictionary containing user UUID and
        correlation ID as extra context.
    """

    def process(self, msg, kwargs):
        return (
            "[%s] [%s] %s"
            % (self.extra["userUUID"], self.extra["correlationID"], msg),
            kwargs,
        )


def get_custom_logger(name, user_uuid="", correlation_id=""):
    """
    Retrieves a custom logger with additional context.

    This function creates a custom logger and sets it up with a stream handler
    and the CustomJsonFormatter. It also sets the log level to INFO.

    Args:
        name (str): The name of the logger.
        userUuid (str, optional): The user UUID for additional context.
        correlationId (str, optional): The correlation ID for additional context.

    Returns:
        CustomLoggerAdapter: The custom logger with additional context.
    """
    handler = logging.StreamHandler()
    handler.setFormatter(CustomJsonFormatter())
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return CustomLoggerAdapter(
        logger, {"userUUID": user_uuid, "correlationID": correlation_id}
    )
