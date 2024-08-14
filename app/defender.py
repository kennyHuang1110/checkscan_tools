import os
import csv
import re
from datetime import datetime

def extract_antivirus_and_hotfix_versions(base_folder_path, csv_file_path):
    """
    Extracts Microsoft Defender Antivirus versions and latest hotfix information from log files in subfolders
    and writes them to a CSV file.

    :param base_folder_path: Path to the base folder containing subfolders with log files.
    :param csv_file_path: Path to the CSV file to write the results.
    """
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['HostName', 'Antivirus Version', 'Latest Hotfix', 'Hotfix Date'])

        for folder_name in os.listdir(base_folder_path):
            folder_path = os.path.join(base_folder_path, folder_name)
            log_file_path = os.path.join(folder_path, 'windowsUpdateListhtml.log')

            if os.path.isfile(log_file_path):
                with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as log_file:
                    antivirus_version = None
                    latest_hotfix = None
                    latest_hotfix_date = None

                    for line in log_file:
                        # Extract Antivirus version
                        if "Microsoft Defender Antivirus" in line:
                            version_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                            if version_match:
                                antivirus_version = "Microsoft Defender Antivirus " + version_match.group(0)

                        # Extract hotfix and date
                        hotfix_match = re.search(r'KB(\d+)', line)
                        date_match = re.search(r'(\d{4}/\d{1,2}/\d{1,2})', line)
                        if hotfix_match and date_match:
                            hotfix = hotfix_match.group(0)
                            hotfix_date = datetime.strptime(date_match.group(0), '%Y/%m/%d')
                            if latest_hotfix_date is None or hotfix_date > latest_hotfix_date:
                                latest_hotfix = hotfix
                                latest_hotfix_date = hotfix_date

                    if antivirus_version is None:
                        antivirus_version = 'Not Found'
                    if latest_hotfix is None:
                        latest_hotfix = 'Not Found'
                    if latest_hotfix_date is None:
                        latest_hotfix_date_str = 'Not Found'
                    else:
                        latest_hotfix_date_str = latest_hotfix_date.strftime('%Y/%m/%d')

                    writer.writerow([folder_name, antivirus_version, latest_hotfix, latest_hotfix_date_str])
                    print(f"Processed folder: {folder_name}")

    print("Processing completed.")

# Example usage
# extract_antivirus_and_hotfix_versions('path/to/base_folder', 'output.csv')
