from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import math


class PDFExporter:
    """Экспортер для сохранения изображений в PDF"""

    @staticmethod
    def export(self, images: List[Image.Image], output_path: str) -> str:
        """Экспортирует список изображений в PDF"""
        if not images:
            raise ValueError("Нет изображений для экспорта")

        # Сохраняем все изображения как одну страницу PDF
        images[0].save(
            output_path,
            "PDF",
            save_all=True,
            append_images=images[1:] if len(images) > 1 else [],
            resolution=100.0
        )

        return output_path
