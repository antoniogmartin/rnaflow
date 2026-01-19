import os
import csv
import re

import pandas as pd
from pathlib import Path


def create_csv_with_data(output_path,path_regex):
    """
    Creates a CSV file with header and example data rows.

    Args:
        output_path: Path where the CSV file will be created
    """
    header = ['Sample', 'R1', 'R2', 'Condition', 'Source', 'Strandedness']

    # Example data rows (modify as needed)

    add_row()
    data = [
        ['sample_001', 'sample_001_R1.fastq.gz', 'sample_001_R2.fastq.gz', 'treatment', 'tissue_A', 'forward'],
        ['sample_002', 'sample_002_R1.fastq.gz', 'sample_002_R2.fastq.gz', 'control', 'tissue_A', 'forward'],
        ['sample_003', 'sample_003_R1.fastq.gz', 'sample_003_R2.fastq.gz', 'treatment', 'tissue_B', 'forward'],
    ]

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

    print(f"✓ CSV file created: {output_path}")
    print(f"Rows added: {len(data)}")


def find_files_regex(folder_path, pattern):
    """
    Finds files matching a regex pattern.

    Args:
        folder_path: Path to the folder to search
        pattern: Regex pattern to match
    """
    regex = re.compile(pattern)
    matching_files = []

    for filename in os.listdir(folder_path):
        if regex.search(filename):
            matching_files.append(filename)

    return matching_files

def regex_find(folder_path,pattern, pattern2, analysis_name):
    matches = find_files_regex(folder_path, pattern)
    matches2 = find_files_regex(folder_path, pattern2)
    matches= matches + matches2

    matrix=[]
    #print(f"Found {len(matches)} matching files:")
    for file in matches:
        parts = file.split('-')

        if "Mock" in file:
            suffix = parts[2].upper()+parts[-1].replace('.fastq.gz', '').upper()
            sample_name = f"{parts[0]}-{suffix}".upper()
        else:
            suffix = parts[-1].replace('.fastq.gz', '').upper()
            sample_name = f"{parts[0]}-{suffix}".upper()
        #print(f"{sample_name}",f"jose-data/{file}",f"{suffix}",",,0")
        matrix.append([sample_name,f"test-data/jose-data/{file}",None,suffix,None,"0"])
    analysis_df = pd.DataFrame(matrix, columns=['Sample', "R1", "R2", "Condition", "Source", "Strandedness"])
    analysis_df.to_csv("../test-data/"+analysis_name, index=False)

def create_analysis_dataset(csv_path, folder_path):
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

    # regex find
    df= pd.read_csv(csv_path)
    for row in df.itertuples():
        input = row.input
        input2 = row.input2
        analysis_name= row.analysis_name
        regex_find(folder_path, input, input2, analysis_name)


if __name__ == "__main__":
    # Configure paths here
    CSV_PATH = "list_of_analysis.csv"  # Path to CSV file
    FOLDER = "../test-data/jose-data"  # Path to folder with files

    create_analysis_dataset(CSV_PATH, FOLDER)