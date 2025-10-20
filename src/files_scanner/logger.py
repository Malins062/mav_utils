import sys

from loguru import logger


def configure_logger():
    logger.remove()  # Удаляем стандартный обработчик
    logger.add(
        "file_scanner.log",  # Лог-файл
        rotation="10 MB",  # Ротация при достижении 10MB
        retention="1 week",  # Хранить логи 1 неделю
        level="INFO",  # Уровень логирования
        encoding="utf-8",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    )
    logger.add(
        sys.stderr,  # Вывод в консоль
        level="INFO",
        format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
    )
