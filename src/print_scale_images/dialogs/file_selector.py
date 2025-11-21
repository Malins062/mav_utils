import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from typing import List


class FileSelector:
    """Класс для выбора файлов и каталогов"""

    @staticmethod
    def select_files() -> List[str]:
        """Выбирает файлы через диалоговое окно"""
        root = tk.Tk()
        root.withdraw()

        file_paths = filedialog.askopenfilenames(
            title="Выберите изображения",
            filetypes=[("Изображения", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"), ("Все файлы", "*.*")],
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
        supported_formats = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif")
        image_files = []
        directory_path = Path(directory)

        for file in directory_path.iterdir():
            if file.is_file() and file.name.lower().endswith(supported_formats):
                image_files.append(str(file))

        return sorted(image_files)
