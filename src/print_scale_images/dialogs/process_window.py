import tkinter as tk
from tkinter import ttk


class ProgressWindow:
    """Окно прогресса для длительных операций"""

    def __init__(self, parent, title="Обработка"):
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("300x100")
        self.window.transient(parent)
        self.window.grab_set()

        # Центрируем окно
        self.window.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.window.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.window.winfo_height()) // 2
        self.window.geometry(f"+{x}+{y}")

        self.label = tk.Label(self.window, text="Обработка...")
        self.label.pack(pady=10)

        self.progress = ttk.Progressbar(self.window, mode="indeterminate")
        self.progress.pack(pady=10, padx=20, fill="x")
        self.progress.start()

    def close(self):
        """Закрывает окно прогресса"""
        self.progress.stop()
        self.window.destroy()
