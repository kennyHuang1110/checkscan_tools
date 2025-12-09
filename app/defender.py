import os
import re
import csv
from datetime import datetime

def extract_antivirus_and_hotfix_versions(base_folder_path, csv_file_path):
    antivirus_regex = re.compile(r'Windows Defender.*?(\d+\.\d+\.\d+\.\d+).*?(\d{4}/\d{1,2}/\d{1,2})')
    hotfix_regex = re.compile(r'KB(\d+).*?(\d{4}/\d{1,2}/\d{1,2})')

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['HostName', 'Antivirus Version', 'Latest Hotfix', 'Hotfix Date'])

        for folder_name in os.listdir(base_folder_path):
            folder_path = os.path.join(base_folder_path, folder_name)
            log_file_path = os.path.join(folder_path, 'windowsUpdateListhtml.log')

            antivirus_version = 'Not Found'
            latest_defender_date = None
            latest_hotfix = 'Not Found'
            latest_hotfix_date = None

            if not os.path.isfile(log_file_path):
                continue

            with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as log_file:
                for line in log_file:
                    if 'Windows Defender' in line:
                        match = antivirus_regex.search(line)
                        if match:
                            version, date_str = match.groups()
                            date_obj = datetime.strptime(date_str, '%Y/%m/%d')
                            if latest_defender_date is None or date_obj > latest_defender_date:
                                antivirus_version = f"Microsoft Defender Antivirus {version} ({date_str})"
                                latest_defender_date = date_obj

                    if 'KB' in line:
                        match = hotfix_regex.search(line)
                        if match:
                            hotfix, date_str = match.groups()
                            date_obj = datetime.strptime(date_str, '%Y/%m/%d')
                            if latest_hotfix_date is None or date_obj > latest_hotfix_date:
                                latest_hotfix = f"KB{hotfix}"
                                latest_hotfix_date = date_obj

            defender_date_str = latest_defender_date.strftime('%Y/%m/%d') if latest_defender_date else 'Not Found'
            hotfix_date_str = latest_hotfix_date.strftime('%Y/%m/%d') if latest_hotfix_date else 'Not Found'

            writer.writerow([folder_name, antivirus_version, latest_hotfix, hotfix_date_str])
            print(f"Processed folder: {folder_name}")

    print("Processing completed.")
