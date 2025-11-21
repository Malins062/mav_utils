from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from loguru import logger
from PIL import Image


@dataclass
class ImageConfig:
    """Конфигурация для вывода изображения"""

    dpi: int = 300
    margin: int = 100
    font_size: int = 40
    font_style: str = "calibri.ttf"
    text_margin: int = 180

    @classmethod
    def from_dict(cls, config_dict: dict[str, Any]) -> ImageConfig:
        """Создает конфиг из словаря"""
        return cls(
            dpi=config_dict.get("dpi", 300),
            margin=config_dict.get("margin", 100),
            font_size=config_dict.get("font_size", 40),
            font_style=config_dict.get("font_style", "calibri.ttf"),
            text_margin=config_dict.get("text_margin", 180),
        )


@dataclass
class LoggerConfig:
    """Конфигурация логгера"""

    filename: str = "processing.log"
    console: bool = False

    @classmethod
    def from_dict(cls, config_dict: dict[str, Any]) -> LoggerConfig:
        """Создает конфиг логгера из словаря"""
        return cls(filename=config_dict.get("filename", "processing.log"), console=config_dict.get("console", False))


@dataclass
class ImageInfo:
    """Информация об обработанном изображении"""

    original_path: str
    original_size: tuple[int, int]
    scaled_size: tuple[int, int]
    scale_ratio: tuple[int, int]
    a4_image: Image.Image


class AppConfig:
    """Основной класс конфигурации приложения"""

    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.image_config: ImageConfig = ImageConfig()
        self.logger_config: LoggerConfig = LoggerConfig()
        self._load_config()

    def _load_config(self) -> None:
        """Загружает конфигурацию из файла"""
        if self.config_path.exists():
            try:
                path = Path(self.config_path)
                with path.open("r", encoding="utf-8") as f:
                    config_data = json.load(f)

                self.image_config = ImageConfig.from_dict(config_data)
                self.logger_config = LoggerConfig.from_dict(config_data)

            except Exception as e:
                logger.error(f"Ошибка загрузки конфигурации: {e}. Используются значения по умолчанию.")
        else:
            self._create_default_config()

    def _create_default_config(self) -> None:
        """Создает файл с конфигурацией по умолчанию"""
        default_config = {
            "dpi": 300,
            "margin": 100,
            "font_size": 40,
            "font_style": "calibri.ttf",
            "text_margin": 180,
            "filename": "processing.log",
            "console": False,
        }

        try:
            path = Path(self.config_path)
            with path.open("w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
            logger.info(f"Создан файл конфигурации по умолчанию: {self.config_path}")
        except Exception as e:
            logger.error(f"Ошибка создания файла конфигурации: {e}")

    def reload(self) -> None:
        """Перезагружает конфигурацию"""
        self._load_config()


# Глобальный экземпляр конфигурации
app_config = AppConfig()
