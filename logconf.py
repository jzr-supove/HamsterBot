import sys
from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <7}</level> | {message}",
    level="TRACE",
    backtrace=True,
    diagnose=True
)
