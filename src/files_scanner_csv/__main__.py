import argparse
import csv
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from loguru import logger

from src.utils import calculate_crc32, configure_logger, get_file_size

# Константа для имени выходного файла
DEFAULT_OUTPUT_FILENAME = "scan_results.csv"


def select_folder():
    """Open folder selection dialog"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    folder_path = filedialog.askdirectory(title="Выберите каталог для сканирования")
    return folder_path


def scan_folder(folder_path, include_subfolders=True):
    """Scan folder and collect PSD and TIF file information"""
    files_data = []
    total_files = 0

    logger.info(f"Starting scan in folder: {folder_path}")
    logger.info(f"Include subfolders: {include_subfolders}")

    folder = Path(folder_path)
    if not folder.exists():
        logger.error(f"Folder does not exist: {folder_path}")
        return files_data, total_files

    # Collect all PSD and TIF files
    psd_files = {}
    tif_files = {}

    if include_subfolders:
        # Scan with subfolders
        pattern_psd = "**/*.psd"
        pattern_tif = "**/*.tif"
    else:
        # Scan only current folder
        pattern_psd = "*.psd"
        pattern_tif = "*.tif"

    # Find PSD files
    for file_path in folder.glob(pattern_psd):
        if file_path.is_file():
            filename = file_path.stem  # filename without extension
            psd_files[filename] = {
                "path": file_path,
                "size": get_file_size(file_path),
                "crc32": calculate_crc32(file_path),
                "folder": file_path.parent.name,
            }
            total_files += 1
            logger.debug(f"Found PSD: {file_path.name}")

    # Find TIF files
    for file_path in folder.glob(pattern_tif):
        if file_path.is_file():
            filename = file_path.stem  # filename without extension
            tif_files[filename] = {
                "path": file_path,
                "size": get_file_size(file_path),
                "crc32": calculate_crc32(file_path),
                "folder": file_path.parent.name,
            }
            total_files += 1
            logger.debug(f"Found TIF: {file_path.name}")

    # Match PSD and TIF files with same names
    all_filenames = set(psd_files.keys()) | set(tif_files.keys())

    for filename in sorted(all_filenames):
        psd_data = psd_files.get(filename)
        tif_data = tif_files.get(filename)

        # Use folder from PSD if available, otherwise from TIF
        folder_name = psd_data["folder"] if psd_data else tif_data["folder"]

        files_data.append(
            {
                "folder_name": folder_name,
                "filename": filename,
                "psd_size": psd_data["size"] if psd_data else 0,
                "psd_crc32": psd_data["crc32"] if psd_data else "",
                "tif_size": tif_data["size"] if tif_data else 0,
                "tif_crc32": tif_data["crc32"] if tif_data else "",
            }
        )

    logger.info(f"Scan completed. Total files processed: {total_files}")
    logger.info(f"Matched file pairs: {len(files_data)}")
    return files_data, total_files


def save_to_csv(files_data, output_file):
    """Save data to CSV file according to template"""
    try:
        output_path = Path(output_file)
        with output_path.open("w", newline="", encoding="utf-8-sig") as csvfile:
            # Write header according to template
            writer = csv.writer(csvfile, delimiter=";")
            writer.writerow(
                [
                    "№",
                    "Машина",
                    "Примечание",
                    "Примечание 2",
                    "Ефимов",
                    "ДСЕ",
                    "ДСЕ имя",
                    "Дата",
                    "Номер диска",
                    "Размер PSD",
                    "На диске PSD",
                    "CRC32 PSD",
                    "Размер TIF",
                    "На диске TIF",
                    "CRC32 TIF",
                    "Занято на CD",
                    "да",
                    "",
                ]
            )

            # Write data rows
            for i, file_data in enumerate(files_data, 1):
                writer.writerow(
                    [
                        i,  # №
                        "",  # Машина
                        "",  # Примечание
                        file_data["folder_name"],  # Примечание 2 / Имя папки
                        "",  # Ефимов
                        file_data["filename"],  # ДСЕ / Имя файла
                        "",  # ДСЕ имя
                        "",  # Дата
                        "",  # Номер диска
                        file_data["psd_size"],  # Размер PSD
                        "",  # На диске PSD
                        file_data["psd_crc32"],  # CRC32 PSD
                        file_data["tif_size"],  # Размер TIF
                        "",  # На диске TIF
                        file_data["tif_crc32"],  # CRC32 TIF
                        "",  # Занято на CD
                        "",  # да
                        "",  # Empty column
                    ]
                )

        logger.success(f"Results successfully saved to: {output_file}")
        return True
    except Exception as e:
        logger.error(f"Error saving to CSV {output_file}: {e}")
        return False


def get_output_filename():
    """Get output filename from command line arguments or use default"""
    parser = argparse.ArgumentParser(description="PSD/TIF File Scanner")
    parser.add_argument(
        "--output",
        "-o",
        default=DEFAULT_OUTPUT_FILENAME,
        help=f"Output CSV filename (default: {DEFAULT_OUTPUT_FILENAME})",
    )

    # Parse only known arguments to avoid conflicts with tkinter
    args, _ = parser.parse_known_args()

    output_file = Path(args.output)

    # If no extension provided, add .csv
    if not output_file.suffix:
        output_file = output_file.with_suffix(".csv")

    # If no directory provided, use current directory
    if not output_file.parent or str(output_file.parent) == ".":
        output_file = Path.cwd() / output_file.name

    return str(output_file)


def main():
    logger.info("=== PSD/TIF File Scanner ===")

    # Get output filename from arguments or use default
    output_file = get_output_filename()
    logger.info(f"Output file: {output_file}")

    # Select folder
    folder_path = select_folder()
    if not folder_path:
        logger.warning("No folder selected. Exiting.")
        return

    logger.info(f"Selected folder: {folder_path}")

    # Check if folder has subfolders
    folder = Path(folder_path)
    has_subfolders = any(item.is_dir() for item in folder.iterdir())

    include_subfolders = True
    if has_subfolders:
        include_subfolders = messagebox.askyesno("Подкаталоги", "Включать в поиск подкаталоги?")

    # Scan files
    logger.info("Scanning PSD and TIF files...")
    files_data, total_files = scan_folder(folder_path, include_subfolders)

    # Save results
    logger.info("Saving results...")
    success = save_to_csv(files_data, output_file)

    # Show summary
    if success:
        messagebox.showinfo(
            "Завершено",
            f"Сканирование завершено!\n"
            f"Найдено файлов: {total_files}\n"
            f"Сопоставлено пар: {len(files_data)}\n"
            f"Результаты сохранены в: {output_file}",
        )
        logger.success(f"Complete! Processed {total_files} files.")
        logger.success(f"Matched {len(files_data)} file pairs.")
        logger.success(f"Results saved to: {output_file}")
    else:
        messagebox.showerror("Ошибка", "Произошла ошибка при сохранении!\nПроверьте лог-файл для деталей.")
        logger.error("Failed to save results!")


if __name__ == "__main__":
    configure_logger()
    main()
