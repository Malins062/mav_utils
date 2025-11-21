import tkinter as tk
from typing import Optional


class ActionDialog:
    """Диалог выбора действия с тремя кнопками"""

    def __init__(self, parent, title: str, processed_count: int):
        self.parent = parent
        self.title = title
        self.processed_count = processed_count
        self.result: Optional[int] = None

        self._create_dialog()

    def _create_dialog(self):
        """Создает диалоговое окно"""

        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.title)
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        # Заголовок
        tk.Label(self.dialog, text=f"Обработано изображений: {self.processed_count}", font=("Arial", 10, "bold")).grid(
            row=0, column=0, columnspan=3, pady=(15, 5), padx=20
        )

        tk.Label(self.dialog, text="Выберите действие:").grid(row=1, column=0, columnspan=3, pady=(0, 15), padx=20)

        # Кнопки
        tk.Button(self.dialog, text="Печать", width=12, command=lambda: self._set_result(1)).grid(
            row=2, column=0, padx=5, pady=10
        )

        tk.Button(self.dialog, text="Экспорт в PDF", width=12, command=lambda: self._set_result(2)).grid(
            row=2, column=1, padx=5, pady=10
        )

        tk.Button(self.dialog, text="Отмена", width=12, command=lambda: self._set_result(3)).grid(
            row=2, column=2, padx=5, pady=10
        )

        # Обновляем окно для расчета размеров
        self.dialog.update_idletasks()

        # Центрируем окно
        x = self.parent.winfo_x() + (self.parent.winfo_width() - self.dialog.winfo_reqwidth()) // 2
        y = self.parent.winfo_y() + (self.parent.winfo_height() - self.dialog.winfo_reqheight()) // 2
        self.dialog.geometry(f"+{x}+{y}")

        # Обработка закрытия окна
        self.dialog.protocol("WM_DELETE_WINDOW", lambda: self._set_result(3))

        # Ждем завершения диалога
        self.parent.wait_window(self.dialog)

    def _set_result(self, action: int):
        """Устанавливает результат и закрывает диалог"""
        self.result = action
        self.dialog.destroy()

    def show(self) -> Optional[int]:
        """Показывает диалог и возвращает результат"""
        return self.result
