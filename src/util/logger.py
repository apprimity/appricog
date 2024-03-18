import os
import logging
from pathlib import Path

log_format = "%(asctime)s - %(levelname)s - %(message)s"
log_level_value = os.environ.get("LOG-LEVEL", logging.NOTSET)

logging.basicConfig(level=log_level_value, format=log_format)
logger = logging.getLogger("ai_framework")