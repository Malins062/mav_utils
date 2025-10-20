import os
import tkinter as tk
from tkinter import filedialog, messagebox
import zlib
import csv
from datetime import datetime


def calculate_crc32(file_path):
    """Calculate CRC32 checksum for a file"""
    try:
        prev = 0
        with open(file_path, "rb") as f:
            for line in f:
                prev = zlib.crc32(line, prev)
        return f"{prev & 0xFFFFFFFF:08X}"
    except Exception as e:
        return f"ERROR: {str(e)}"


def get_file_size_kb(file_path):
    """Get file size in KB"""
    try:
        size_bytes = os.path.getsize(file_path)
        return round(size_bytes / 1024, 2)
    except:
        return 0


def get_file_date(file_path):
    """Get file modification date"""
    try:
        timestamp = os.path.getmtime(file_path)
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except:
        return "Unknown"


def select_folder():
    """Open folder selection dialog"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    folder_path = filedialog.askdirectory(title="Select folder to scan")
    return folder_path


def scan_folder(folder_path, include_subfolders=True):
    """Scan folder and collect file information"""
    files_data = []
    total_files = 0

    if include_subfolders:
        # Scan with subfolders
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                files_data.append(process_file(file_path))
                total_files += 1
                print(f"Processed: {file}")
    else:
        # Scan only current folder
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                files_data.append(process_file(item_path))
                total_files += 1
                print(f"Processed: {item}")

    return files_data, total_files


def process_file(file_path):
    """Process individual file and return its data"""
    return {
        "path": file_path,
        "size_kb": get_file_size_kb(file_path),
        "crc32": calculate_crc32(file_path),
        "modified": get_file_date(file_path),
    }


def save_to_csv(files_data, output_file):
    """Save data to CSV file"""
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["File", "Size_KB", "CRC32", "LastModified"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")

        writer.writeheader()
        for file_data in files_data:
            writer.writerow(
                {
                    "File": file_data["path"],
                    "Size_KB": file_data["size_kb"],
                    "CRC32": file_data["crc32"],
                    "LastModified": file_data["modified"],
                }
            )


def main():
    print("=== File Scanner with CRC32 ===")

    # Select folder
    folder_path = select_folder()
    if not folder_path:
        print("No folder selected. Exiting.")
        return

    print(f"Selected folder: {folder_path}")

    # Ask for subfolders
    include_subfolders = messagebox.askyesno("Subfolders", "Include subfolders?")

    # Ask for output file
    output_file = filedialog.asksaveasfilename(
        title="Save results as CSV", defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )

    if not output_file:
        print("No output file selected. Exiting.")
        return

    # Scan files
    print("Scanning files...")
    files_data, total_files = scan_folder(folder_path, include_subfolders)

    # Save results
    print("Saving results...")
    save_to_csv(files_data, output_file)

    # Show summary
    messagebox.showinfo(
        "Complete", f"Scanning complete!\n" f"Files processed: {total_files}\n" f"Results saved to: {output_file}"
    )

    print(f"\nComplete! Processed {total_files} files.")
    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    main()
