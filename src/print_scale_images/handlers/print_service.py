import os
import platform
import tempfile
import time
from pathlib import Path
from typing import List

from loguru import logger

from src.print_scale_images.config import ImageInfo
from src.print_scale_images.handlers.pdf_exporter import PDFExporter


class PrinterService:
    """Кроссплатформенный сервис для работы с печатью"""

    def print_images(self, processed_images: List[ImageInfo]) -> bool:
        """Печатает список обработанных изображений через временный PDF"""

        temp_path = None
        try:
            # Создаем временный PDF файл
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                temp_path = temp_file.name

            # Сохраняем PDF
            PDFExporter().export_to_pdf(processed_images, temp_path)

            # Печатаем PDF средствами ОС
            success = self._print_pdf(temp_path)

            # Задержка перед удалением файла (особенно для Windows)
            if success and platform.system() == "Windows":
                time.sleep(5)  # 5 секунд для Windows
            elif success:
                time.sleep(2)  # 2 секунды для других ОС

            return success

        except Exception as e:
            logger.error(f"Ошибка печати: {e}")
            return False
        finally:
            # Удаляем временный файл после задержки
            path = Path(temp_path)
            if temp_path and path.exists():
                try:
                    path.unlink()
                    logger.debug(f"Временный файл удален: {temp_path}")
                except Exception as e:
                    logger.warning(f"Не удалось удалить временный файл {temp_path}: {e}")

    @staticmethod
    def _print_pdf(pdf_path: str) -> bool:
        """Печатает PDF файл средствами ОС"""

        try:
            system = platform.system()
            logger.debug(f"Печать PDF на системе: {system}, файл: {pdf_path}")

            if system == "Windows":
                os.startfile(pdf_path, "print")
                logger.debug("Команда печати отправлена в Windows")
                return True
            elif system == "Darwin":  # macOS
                result = os.system(f'lpr "{pdf_path}"')
                logger.debug(f"Команда lpr выполнена с кодом: {result}")
                return result == 0
            elif system == "Linux":
                result = os.system(f'lpr "{pdf_path}"')
                logger.debug(f"Команда lpr выполнена с кодом: {result}")
                return result == 0
            else:
                logger.error(f"Не поддерживаемая платформа: {system}")
                return False

        except Exception as e:
            logger.error(f"Ошибка печати PDF: {e}")
            return False
