import configparser

config = configparser.ConfigParser()
config.read("config.ini")
client = config["CLIENT"]

AUTH_TOKEN = client["AUTH_TOKEN"]
USER_AGENT = client["USER_AGENT"]
SEC_CH_UA = client["SEC_CH_UA"]
DEBUG = client["DEBUG"].lower() in {"true", "1", "on"}

del config, client


def configure_logger(level: str = "INFO"):
    import sys
    from loguru import logger

    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <7}</level> | {message}",
        level=level,
        backtrace=True,
        diagnose=True
    )
