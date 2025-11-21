import os
import platform
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import List, Optional

from loguru import logger

from src.print_scale_images.config import ImageInfo
from src.print_scale_images.dialogs.actions import ActionDialog
from src.print_scale_images.dialogs.file_selector import FileSelector
from src.print_scale_images.dialogs.process_window import ProgressWindow
from src.print_scale_images.handlers.caption_builder import CaptionBuilder
from src.print_scale_images.handlers.image_service import ImageProcessingService
from src.print_scale_images.handlers.pdf_exporter import PDFExporter
from src.print_scale_images.handlers.print_service import PrinterService
from src.utils.files import get_filename_without_extension


class MainController:
    """Контроллер для управления UI и бизнес-логикой"""

    def __init__(self):
        self.process_service = ImageProcessingService()
        self.file_selector = FileSelector()
        self.printer_service = PrinterService()
        self.root = tk.Tk()
        self._setup_ui()

    def _setup_ui(self):
        """Настраивает пользовательский интерфейс"""

        self.root.title("Экспорт изображений на A4")
        self.root.geometry("450x200")

        # Основные кнопки
        self.btn_files = tk.Button(self.root, text="Выбрать файлы для обработки", command=self.process_files, height=2)
        self.btn_files.pack(pady=10, fill="x", padx=20)

        self.btn_directory = tk.Button(
            self.root, text="Выбрать папку для обработки", command=self.process_directory, height=2
        )
        self.btn_directory.pack(pady=10, fill="x", padx=20)

        # Информационная метка
        self.info_label = tk.Label(
            self.root,
            text="Изображения автоматически масштабируются для вписывания в A4\n"
            "Используются целочисленные масштабы (1:2, 1:2.5, 1:4, 1.5)\n"
            "После обработки можно напечатать или сохранить в PDF",
            wraplength=400,
            justify="center",
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
            processed_images = self.process_service.process_images(image_paths)

            if not processed_images:
                text = "Не удалось обработать ни одного изображения"
                messagebox.showerror("Ошибка", text)
                logger.error(text)
                return

            # Логируем результаты
            self._log_results(processed_images)

            # # Показываем краткие результаты
            # self._show_brief_results(processed_images)

            # Диалог выбора действия
            action = self._show_action_dialog(len(processed_images))
            match action:
                case 1:
                    self._print_images(processed_images)
                case 2:
                    self._save_to_pdf(processed_images)
            # Если 3 (Отмена) или закрыто окно - ничего не делаем

        except Exception as e:
            text = f"Произошла ошибка: {str(e)}"
            messagebox.showerror("Ошибка", text)
            logger.error(text)
        finally:
            progress_window.close()

    def _show_action_dialog(self, processed_count: int) -> int:
        """Показывает диалог выбора действия"""

        dialog = ActionDialog(self.root, "Выберите действие", processed_count)
        return dialog.result if dialog.result else 3  # По умолчанию Отмена

    def _print_images(self, processed_images: List[ImageInfo]):
        """Печатает обработанные изображения"""

        try:
            success = self.printer_service.print_images(processed_images)
            if success:
                messagebox.showinfo("Печать", "Изображения отправлены на печать!")
            else:
                messagebox.showwarning("Печать", "Не удалось выполнить печать")
        except Exception as e:
            messagebox.showerror("Ошибка печати", f"Ошибка при печати: {str(e)}")
            logger.error(f"Print error: {e}")

    def _save_to_pdf(self, processed_images: List[ImageInfo]):
        """Сохраняет обработанные изображения в PDF"""

        output_path = self._select_output_path()
        if not output_path:
            return

        try:
            result_path = PDFExporter().export_to_pdf(processed_images, output_path)
            messagebox.showinfo("Сохранение", f"PDF успешно сохранен:\n{result_path}")

            # Предложение открыть результат
            if messagebox.askyesno("Открыть файл", "Хотите открыть полученный PDF файл?"):
                self._open_file(result_path)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении PDF: {str(e)}")
            logger.error(f"PDF export error: {e}")

    @staticmethod
    def _open_file(file_path: str):
        """Открывает файл средствами ОС"""
        try:
            path = Path(file_path).resolve()
            system_name = platform.system()

            if system_name == "Windows":
                os.startfile(path)  # noqa
            elif system_name == "Darwin":  # macOS
                os.system(f'open "{path}"')
            else:  # Linux
                os.system(f'xdg-open "{path}"')
        except Exception as e:
            logger.error(f"Error opening file: {e}")

    @staticmethod
    def _select_output_path() -> Optional[str]:
        """Выбирает путь для сохранения PDF"""
        root = tk.Tk()
        root.withdraw()

        output_path = filedialog.asksaveasfilename(
            title="Сохранить PDF как", defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
        )
        root.destroy()

        return output_path

    @staticmethod
    def _show_brief_results(processed_images: List[ImageInfo]):
        """Показывает краткие результаты обработки"""
        result_info = f"Обработка завершена!\nОбработано изображений: {len(processed_images)}"
        messagebox.showinfo("Результат", result_info)

    @staticmethod
    def _log_results(processed_images: List[ImageInfo]):
        """Показывает результаты обработки"""

        extended_result_info = f"Обработка завершена успешно!\n\n" f"Обработано изображений: {len(processed_images)}\n"

        for info in processed_images:
            filename = get_filename_without_extension(info.original_path)

            orig_w, orig_h = info.original_size
            scaled_w, scaled_h = info.scaled_size
            extended_result_info += (
                f"• {filename}: {orig_w}x{orig_h} → {scaled_w}x{scaled_h} "
                f"({CaptionBuilder().generate_caption_ratio(info.scale_ratio)})\n"
            )

        logger.info(extended_result_info)

    def run(self):
        """Запускает приложение"""
        self.root.mainloop()
