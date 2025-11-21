import sys

from loguru import logger


def configure_logger(file_name=None, console=True):
    logger.remove()  # Удаляем стандартный обработчик
    if file_name:
        logger.add(
            file_name,  # Лог-файл
            rotation="10 MB",  # Ротация при достижении 10MB
            retention="1 week",  # Хранить логи 1 неделю
            level="INFO",  # Уровень логирования
            encoding="utf-8",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        )
    if console:
        logger.add(
            sys.stderr,  # Вывод в консоль
            level="INFO",
            format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
        )
