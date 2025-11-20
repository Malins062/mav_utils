from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import math


class FileSelector:
    """Класс для выбора файлов и каталогов"""

    @staticmethod
    def select_files() -> List[str]:
        """Выбирает файлы через диалоговое окно"""
        root = tk.Tk()
        root.withdraw()

        file_paths = filedialog.askopenfilenames(
            title="Выберите изображения",
            filetypes=[
                ("Изображения", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
                ("Все файлы", "*.*")
            ]
        )
        root.destroy()

        return list(file_paths)

    @staticmethod
    def select_directory() -> List[str]:
        """Выбирает все изображения из каталога"""
        root = tk.Tk()
        root.withdraw()

        directory = filedialog.askdirectory(title="Выберите папку с изображениями")
        root.destroy()

        if not directory:
            return []

        # Поддерживаемые форматы изображений
        supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')
        image_files = []

        for file in os.listdir(directory):
            if file.lower().endswith(supported_formats):
                image_files.append(os.path.join(directory, file))

        return sorted(image_files)