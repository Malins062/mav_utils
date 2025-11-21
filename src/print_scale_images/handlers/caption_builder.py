from PIL import Image, ImageDraw, ImageFont

from src.print_scale_images.config import ImageConfig
from src.utils.files import get_filename_without_extension


class CaptionBuilder:
    """Строитель для добавления подписей к изображениям"""

    def __init__(self):
        self._font_cache = {}

    def add_caption(
        self, image: Image.Image, image_path: str, scale_ratio: tuple[int, int], config: ImageConfig
    ) -> Image.Image:
        """Добавляет подпись к изображению"""
        draw = ImageDraw.Draw(image)
        font = self._get_font(config.font_size)

        # Генерируем текст подписи
        caption = self._generate_caption(image_path, scale_ratio)

        # Позиционируем текст по центру внизу
        text_x = image.width // 2
        text_y = image.height - config.text_margin // 2

        draw.text((text_x, text_y), caption, fill="black", font=font, anchor="mm")
        return image

    @staticmethod
    def _generate_caption(image_path: str, scale_ratio: tuple[int, int]) -> str:
        """Генерирует текст подписи"""
        filename = get_filename_without_extension(image_path)
        denominator, numerator = scale_ratio

        if denominator == 1 and numerator == 1:
            scale_text = "оригинал"
        else:
            scale_text = f"1:{denominator}"

        return f"{filename} - масштаб: {scale_text}"

    def _get_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Получает шрифт (с кэшированием)"""

        if size not in self._font_cache:
            self._font_cache[size] = self._load_font(size)
        return self._font_cache[size]

    @staticmethod
    def _load_font(size: int) -> ImageFont.FreeTypeFont:
        """Загружает шрифт с fallback'ами"""

        font_paths = ["arial.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"]

        for font_path in font_paths:
            try:
                return ImageFont.truetype(font_path, size)
            except OSError:
                continue

        return ImageFont.load_default()
