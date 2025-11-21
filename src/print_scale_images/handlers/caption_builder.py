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
        font = self._get_font(config.font_size, config.font_style)

        # Генерируем текст подписи
        caption = self._generate_caption(image_path, scale_ratio)

        # Позиционируем текст по центру внизу
        text_x = image.width // 2
        text_y = image.height - config.text_margin // 2

        draw.text((text_x, text_y), caption, fill="black", font=font, anchor="mm")
        return image

    @classmethod
    def _generate_caption(cls, image_path: str, scale_ratio: tuple[int, int]) -> str:
        """Генерирует текст подписи"""

        filename = get_filename_without_extension(image_path)

        return f"{filename} {cls.generate_caption_ratio(scale_ratio)}"

    @classmethod
    def generate_caption_ratio(cls, scale_ratio: tuple[int, int]) -> str:
        """Генерирует текст масштаба"""

        denominator, numerator = scale_ratio

        if denominator == 1 and numerator == 1:
            scale_text = "1:1"
        elif denominator == 5 and numerator == 2:
            scale_text = "1:2.5"
        else:
            scale_text = f"1:{denominator}"

        return f"Масштаб: {scale_text}"

    def _get_font(self, size: int, font_style: str) -> ImageFont.FreeTypeFont:
        """Получает шрифт (с кэшированием)"""

        cache_key = f"{font_style}_{size}"
        if cache_key not in self._font_cache:
            self._font_cache[cache_key] = self._load_font(size, font_style)
        return self._font_cache[cache_key]

    @staticmethod
    def _load_font(size: int, preferred_font: str) -> ImageFont.FreeTypeFont:
        """Загружает шрифт с fallback'ами"""

        font_paths = (
            preferred_font,
            "arial.ttf",
            "DejaVuSans.ttf",
            "LiberationSans-Regular.ttf",
        )

        for font_path in font_paths:
            try:
                return ImageFont.truetype(font_path, size)
            except OSError:
                continue

        return ImageFont.load_default()
