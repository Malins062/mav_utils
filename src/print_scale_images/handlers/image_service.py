from typing import List

from loguru import logger
from PIL import Image

from src.print_scale_images.config import ImageInfo, app_config
from src.print_scale_images.handlers.caption_builder import CaptionBuilder
from src.print_scale_images.handlers.image_processor import A4ImageProcessor


class ImageProcessingService:
    """Сервис для управления процессом печати"""

    def __init__(self):
        self.image_processor = A4ImageProcessor()
        self.caption_builder = CaptionBuilder()
        self.config = app_config.image_config

    def process_images(self, image_paths: List[str]) -> List[ImageInfo]:
        """Обрабатывает список изображений"""

        processed_images = []

        for image_path in image_paths:
            try:
                with Image.open(image_path) as original_image:
                    # Обрабатываем изображение
                    image_info = self.image_processor.process(original_image, self.config)
                    image_info.original_path = image_path

                    # Добавляем подпись
                    image_info.a4_image = self.caption_builder.add_caption(
                        image_info.a4_image, image_path, image_info.scale_ratio, self.config
                    )

                    processed_images.append(image_info)

            except Exception as e:
                logger.error(f"Ошибка обработки {image_path}: {e}")
                continue

        return processed_images
