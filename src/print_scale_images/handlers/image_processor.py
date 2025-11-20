from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import math


class ImageProcessor(ABC):
    """Абстрактный класс для обработки изображений"""

    @abstractmethod
    def process(self, image: Image.Image, config: PrintConfig) -> ImageInfo:
        pass



class A4PrintProcessor(ImageProcessor):
    """Обработчик для подготовки изображений к печати на A4"""

    def __init__(self):
        # A4 в альбомной ориентации 300 DPI: 297mm x 210mm
        self.a4_size_landscape = (3508, 2480)  # высота x ширина
        self.scale_calculator = ScaleCalculator()

    def process(self, image: Image.Image, config: PrintConfig) -> ImageInfo:
        """Обрабатывает изображение для печати на A4"""
        scaled_image, scale_ratio = self._scale_image(image, config)
        a4_image = self._create_a4_page(scaled_image, config)

        return ImageInfo(
            original_path="",
            original_size=image.size,
            scaled_size=scaled_image.size,
            scale_ratio=scale_ratio,
            a4_image=a4_image
        )

    def _scale_image(self, image: Image.Image, config: PrintConfig) -> Tuple[Image.Image, Tuple[int, int]]:
        """Масштабирует изображение для вписывания в A4 с целочисленными коэффициентами"""
        # Максимальный размер с учетом отступов и места для подписи
        max_width = self.a4_size_landscape[0] - 2 * config.margin
        max_height = self.a4_size_landscape[1] - 2 * config.margin - config.text_margin

        scale, scale_ratio = self.scale_calculator.calculate_best_scale(
            image.size,
            (max_width, max_height)
        )

        new_size = (int(image.width * scale), int(image.height * scale))
        scaled_image = image.resize(new_size, Image.LANCZOS)

        return scaled_image, scale_ratio

    def _create_a4_page(self, image: Image.Image, config: PrintConfig) -> Image.Image:
        """Создает страницу A4 с изображением"""
        a4_image = Image.new('RGB', self.a4_size_landscape, 'white')

        # Центрируем изображение
        x = (self.a4_size_landscape[0] - image.width) // 2
        y = (self.a4_size_landscape[1] - image.height - config.text_margin) // 2

        a4_image.paste(image, (x, y))
        return a4_image
