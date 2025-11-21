from dataclasses import dataclass

from PIL import Image


@dataclass
class ImageConfig:
    """Конфигурация для вывода изображения"""

    dpi: int = 300
    margin: int = 100
    font_size: int = 40
    text_margin: int = 180


@dataclass
class ImageInfo:
    """Информация об обработанном изображении"""

    original_path: str
    original_size: tuple[int, int]
    scaled_size: tuple[int, int]
    scale_ratio: tuple[int, int]  # (1, 2) для масштаба 1:2
    a4_image: Image.Image


@dataclass
class LoggerConfig:
    """Основная конфигурация"""

    filename: str = "processing.log"
    console: bool = False
