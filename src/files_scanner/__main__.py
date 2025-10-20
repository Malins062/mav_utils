import csv
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from loguru import logger

from src.utils import calculate_crc32, configure_logger, get_file_date, get_file_size


def select_folder():
    """Open folder selection dialog"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    folder_path = filedialog.askdirectory(title="Выберите каталог для сканирования")
    return folder_path


def scan_folder(folder_path, include_subfolders=True):
    """Scan folder and collect file information"""
    files_data = []
    total_files = 0

    logger.info(f"Starting scan in folder: {folder_path}")
    logger.info(f"Include subfolders: {include_subfolders}")

    folder = Path(folder_path)
    if not folder.exists():
        logger.error(f"Folder does not exist: {folder_path}")
        return files_data, total_files

    if include_subfolders:
        # Scan with subfolders using pathlib
        for file_path in folder.rglob("*"):
            if file_path.is_file():
                files_data.append(process_file(file_path))
                total_files += 1
                logger.debug(f"Processed: {file_path.name}")

                # Логируем прогресс каждые 100 файлов
                if total_files % 100 == 0:
                    logger.info(f"Processed {total_files} files...")
    else:
        # Scan only current folder
        for item in folder.iterdir():
            if item.is_file():
                files_data.append(process_file(item))
                total_files += 1
                logger.debug(f"Processed: {item.name}")

    logger.info(f"Scan completed. Total files: {total_files}")
    return files_data, total_files


def process_file(file_path):
    """Process individual file and return its data"""
    try:
        file_data = {
            "path": file_path,
            "size": get_file_size(file_path),
            "crc32": calculate_crc32(file_path),
            "modified": get_file_date(file_path),
        }
        return file_data
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        return {
            "path": file_path,
            "size": 0,
            "crc32": "ERROR",
            "modified": "Unknown",
        }


def save_to_csv(files_data, output_file):
    """Save data to CSV file"""
    try:
        output_path = Path(output_file)
        with output_path.open("w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["File", "Size", "CRC32", "LastModified"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")

            writer.writeheader()
            for file_data in files_data:
                writer.writerow(
                    {
                        "File": file_data["path"],
                        "Size": file_data["size"],
                        "CRC32": file_data["crc32"],
                        "LastModified": file_data["modified"],
                    }
                )
        logger.success(f"Results successfully saved to: {output_file}")
        return True
    except Exception as e:
        logger.error(f"Error saving to CSV {output_file}: {e}")
        return False


def main():
    logger.info("=== File Scanner with CRC32 ===")

    # Select folder
    folder_path = select_folder()
    if not folder_path:
        logger.warning("No folder selected. Exiting.")
        return

    logger.info(f"Selected folder: {folder_path}")

    # Ask for subfolders
    include_subfolders = messagebox.askyesno("Подкаталоги", "Включать в поиск подкаталоги?")

    # Ask for output file
    output_file = filedialog.asksaveasfilename(
        title="Сохранить результаты в CSV",
        defaultextension=".csv",
        filetypes=[("CSV файлы", "*.csv"), ("Все файлы", "*.*")],
    )

    if not output_file:
        logger.warning("No output file selected. Exiting.")
        return

    # Scan files
    logger.info("Scanning files...")
    files_data, total_files = scan_folder(folder_path, include_subfolders)

    # Save results
    logger.info("Saving results...")
    success = save_to_csv(files_data, output_file)

    # Show summary
    if success:
        messagebox.showinfo(
            "Завершено",
            f"Сканирование завершено!\n" f"Обработано файлов: {total_files}\n" f"Результаты сохранены в: {output_file}",
        )
        logger.success(f"Complete! Processed {total_files} files.")
        logger.success(f"Results saved to: {output_file}")
    else:
        messagebox.showerror("Ошибка", "Произошла ошибка при сохранении!\n" "Проверьте лог-файл для деталей.")
        logger.error("Failed to save results!")


if __name__ == "__main__":
    configure_logger()
    main()
