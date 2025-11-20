from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import math




class PrintService:
    """Сервис для управления процессом печати"""

    def __init__(self):
        self.image_processor = A4PrintProcessor()
        self.caption_builder = CaptionBuilder()
        self.pdf_exporter = PDFExporter()
        self.config = PrintConfig()

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
                        image_info.a4_image,
                        image_path,
                        image_info.scale_ratio,
                        self.config
                    )

                    processed_images.append(image_info)

            except Exception as e:
                print(f"Ошибка обработки {image_path}: {e}")
                continue

        return processed_images

    def export_to_pdf(self, image_infos: List[ImageInfo], output_path: str) -> str:
        """Экспортирует обработанные изображения в PDF"""
        images = [info.a4_image for info in image_infos]
        return self.pdf_exporter.export(images, output_path)