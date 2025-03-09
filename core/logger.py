import json
import logging
import os
from datetime import date
from datetime import datetime
from functools import lru_cache
from typing import Any
from typing import Optional

from pythonjsonlogger import jsonlogger

try:
    import pydantic
except ImportError:
    pydantic = None


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


class MyJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if pydantic is not None and isinstance(o, pydantic.BaseModel):
            return json.loads(o.json())

        if isinstance(o, datetime) or isinstance(o, date):
            return o.isoformat()

        return str(o)


class CustomLogger(logging.Logger):
    _instance = None

    def __new__(cls, name: Optional[str] = None):
        if cls._instance is None:
            if name is None:
                name = "conversational_agent"
            logger = logging.getLogger(name=name)
            logger.setLevel(os.getenv("DEBUG_LEVEL", "INFO"))
            formatter = CustomJsonFormatter(
                "%(timestamp)s %(level)s %(name)s %(funcName)s %(message)s",
                json_encoder=MyJSONEncoder,
            )

            if logger.hasHandlers():
                for handler in logger.handlers:
                    handler.setFormatter(formatter)
            else:
                handler = logging.StreamHandler()
                handler.setFormatter(formatter)
                logger.addHandler(handler)
            cls._instance = logger

        return cls._instance
    
@lru_cache
def get_logger(name: Optional[str] = None) -> logging.Logger:
    return CustomLogger(name=name)