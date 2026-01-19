import os
import csv
from pathlib import Path


def rename_files(csv_path, folder_path):
    """
    Renames files in a folder according to a CSV mapping.

    Args:
        csv_path: Path to the CSV file with the mapping
        folder_path: Path to the folder containing files to rename
    """
    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist")
        return

    # Check if CSV exists
    if not os.path.exists(csv_path):
        print(f"Error: CSV file '{csv_path}' does not exist")
        return

    # Read CSV and create mapping
    renamed_count = 0
    error_count = 0

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        for row_num, row in enumerate(reader, 1):
            if len(row) < 2:
                print(f"Warning: Row {row_num} doesn't have 2 columns, skipping")
                continue

            original_name = row[0].strip()
            target_name = row[1].strip()

            # Add .fastq.gz extension
            original_file = os.path.join(folder_path, f"{original_name}.fastq.gz")
            target_file = os.path.join("../test-data/jose-data", f"{target_name}.fastq.gz")

            # Check if original file exists
            if not os.path.exists(original_file):
                print(f"Warning: File '{original_file}' not found")
                error_count += 1
                continue

            # Check if target file already exists
            if os.path.exists(target_file):
                print(f"Warning: '{target_file}' already exists, skipping")
                error_count += 1
                continue

            # Rename the file
            try:
                os.rename(original_file, target_file)
                print(f"✓ Renamed: {original_name}.fastq.gz → {target_name}.fastq.gz")
                renamed_count += 1
            except Exception as e:
                print(f"Error renaming '{original_file}': {e}")
                error_count += 1

    # Summary
    print(f"\n{'=' * 50}")
    print(f"Files renamed: {renamed_count}")
    print(f"Errors/Skipped: {error_count}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    # Configure paths here
    CSV_PATH = "../legend_data.csv"  # Path to CSV file
    FOLDER = "../raw_reads"  # Path to folder with files

    rename_files(CSV_PATH, FOLDER)