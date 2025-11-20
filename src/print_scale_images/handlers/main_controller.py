from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import math


class MainController:
    """Контроллер для управления UI и бизнес-логикой"""

    def __init__(self):
        self.print_service = PrintService()
        self.file_selector = FileSelector()
        self.root = tk.Tk()
        self._setup_ui()

    def _setup_ui(self):
        """Настраивает пользовательский интерфейс"""
        self.root.title("Печать изображений на A4")
        self.root.geometry("450x250")

        # Основные кнопки
        self.btn_files = tk.Button(
            self.root,
            text="Выбрать файлы для обработки",
            command=self.process_files,
            height=2
        )
        self.btn_files.pack(pady=10, fill='x', padx=20)

        self.btn_directory = tk.Button(
            self.root,
            text="Выбрать папку для обработки",
            command=self.process_directory,
            height=2
        )
        self.btn_directory.pack(pady=10, fill='x', padx=20)

        # Информационная метка
        self.info_label = tk.Label(
            self.root,
            text="Изображения автоматически масштабируются для вписывания в A4\n"
                 "Используются целочисленные масштабы (1:2, 1:3, 1:4...)\n"
                 "Результат сохраняется в PDF файл",
            wraplength=400,
            justify='center'
        )
        self.info_label.pack(pady=10)

    def process_files(self):
        """Обработка выбранных файлов"""
        self._process_images(self.file_selector.select_files())

    def process_directory(self):
        """Обработка всей папки"""
        image_paths = self.file_selector.select_directory()
        if image_paths:
            self._process_images(image_paths)

    def _process_images(self, image_paths: List[str]):
        """Основной метод обработки изображений"""
        if not image_paths:
            return

        # Показываем прогресс
        progress_window = ProgressWindow(self.root, f"Обработка {len(image_paths)} изображений")
        self.root.update()

        try:
            # Обработка изображений
            processed_images = self.print_service.process_images(image_paths)

            if not processed_images:
                messagebox.showerror("Ошибка", "Не удалось обработать ни одного изображения")
                return

            # Выбор места сохранения
            output_path = self._select_output_path()
            if not output_path:
                return

            # Экспорт в PDF
            result_path = self.print_service.export_to_pdf(processed_images, output_path)

            # Показ результатов
            self._show_results(processed_images, result_path)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
        finally:
            progress_window.close()

    def _select_output_path(self) -> Optional[str]:
        """Выбирает путь для сохранения PDF"""
        root = tk.Tk()
        root.withdraw()

        output_path = filedialog.asksaveasfilename(
            title="Сохранить PDF как",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        root.destroy()

        return output_path

    def _show_results(self, processed_images: List[ImageInfo], result_path: str):
        """Показывает результаты обработки"""
        filename_helper = FilenameHelper()

        result_info = (
            f"Обработка завершена успешно!\n\n"
            f"Обработано изображений: {len(processed_images)}\n"
            f"PDF файл: {os.path.basename(result_path)}\n\n"
            f"Детали масштабирования:\n"
        )

        for info in processed_images:
            filename = filename_helper.get_filename_without_extension(info.original_path)
            denominator, numerator = info.scale_ratio
            scale_text = "оригинал" if denominator == 1 and numerator == 1 else f"1:{denominator}"

            orig_w, orig_h = info.original_size
            scaled_w, scaled_h = info.scaled_size
            result_info += f"• {filename}: {orig_w}x{orig_h} → {scaled_w}x{scaled_h} ({scale_text})\n"

        messagebox.showinfo("Результат", result_info)

        # Предложение открыть результат
        if messagebox.askyesno("Открыть файл", "Хотите открыть полученный PDF файл?"):
            try:
                os.startfile(result_path)  # Windows
            except:
                try:
                    import subprocess
                    subprocess.run(['xdg-open', result_path])  # Linux
                except:
                    pass

    def run(self):
        """Запускает приложение"""
        self.root.mainloop()
