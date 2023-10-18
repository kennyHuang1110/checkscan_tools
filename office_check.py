import csv
import re
import os

def extract_office_data(source_folder_path, target_folder_name):
    target_folder_path = os.path.join(source_folder_path, target_folder_name)

    if not os.path.exists(target_folder_path):
        os.makedirs(target_folder_path)

    folder_names = [name for name in os.listdir(source_folder_path) if os.path.isdir(os.path.join(source_folder_path, name))]

    with open(os.path.join(target_folder_path, 'office.csv'), mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['folder_name', 'office_version'])

        for folder_name in folder_names:
            file_path = os.path.join(source_folder_path, folder_name, 'productlist.log')

            if not os.path.exists(file_path):
                csv_writer.writerow([folder_name, 'None'])
                continue

            with open(file_path, 'r', encoding='utf-16') as log_file:
                lines = log_file.readlines()

                office_info = None
                filter_conditions = [
                   'Microsoft Office Standard ',
                    'Office 16 Click-to-Run',
                "Microsoft Office Professional Plus",
                    ]

                for line in lines:
                    clean_line = line.strip()
                    if clean_line and not clean_line.startswith('Caption'):
                        data = re.split(r'\s{2,}', clean_line)
                        if len(data) >= 5:
                            name = data[2].strip()
                            version = data[4].strip()
                            for condition in filter_conditions:
                                if condition in name:
                                    office_info = f"{name} {version}"
                                    break
                            else:
                                continue
                            break
                csv_writer.writerow([folder_name, office_info if office_info else 'None'])

    print(f"已生成 {target_folder_name}/office.csv 檔。")


