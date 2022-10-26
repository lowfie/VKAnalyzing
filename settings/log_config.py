from loguru import logger

# Базовые настройки логирования
logger.add(
    "logs/{time:YYYY-MM-DD} logs.log",
    format="{time} : {level} : {message}",
    level="INFO",
    rotation="1 day",
)
