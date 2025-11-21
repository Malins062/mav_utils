from loguru import logger
from PIL import Image

from src.print_scale_images.config import ImageInfo


class PDFExporter:
    """Экспортер для сохранения изображений в PDF"""

    @classmethod
    def export(cls, images: list[Image.Image], output_path: str) -> str:
        """Экспортирует список изображений в PDF"""
        if not images:
            text = "Нет изображений для экспорта"
            logger.error(text)
            raise ValueError(text)

        # Сохраняем все изображения как одну страницу PDF
        images[0].save(
            output_path, "PDF", save_all=True, append_images=images[1:] if len(images) > 1 else [], resolution=100.0
        )

        return output_path

    @classmethod
    def export_to_pdf(cls, image_infos: list[ImageInfo], output_path: str) -> str:
        """Экспортирует обработанные изображения в PDF"""
        images = [info.a4_image for info in image_infos]
        return cls.export(images, output_path)
