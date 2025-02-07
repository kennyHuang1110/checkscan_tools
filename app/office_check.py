import csv
import re
import os

def extract_software_data(source_folder_path, target_folder_path):
    """
    從 productlist.log 提取 Microsoft Office、Flash、Adobe Reader 等軟體資訊，並存為 office.csv。
    
    :param source_folder_path: 來源資料夾 (通常為 data/檢視S)
    :param target_folder_path: 儲存目標資料夾 (通常為 data/檢視productlist_OFFICE)
    """
    # 確保目標資料夾存在
    if not os.path.exists(target_folder_path):
        os.makedirs(target_folder_path)
        print(f"📂 目標資料夾已創建: {target_folder_path}")

    # 設定 CSV 檔案路徑
    office_csv_path = os.path.join(target_folder_path, 'office.csv')

    # 讀取 source_folder_path 內的所有子資料夾
    folder_names = [name for name in os.listdir(source_folder_path) if os.path.isdir(os.path.join(source_folder_path, name))]

    with open(office_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['HostName', 'office_version', 'flash_version', 'acrobat_version', 'reader_version', 'java_version'])

        for folder_name in folder_names:
            file_path = os.path.join(source_folder_path, folder_name, 'productlist.log')

            # 預設所有軟體的資訊為 'None'
            software_info = {
                'office': 'None',
                'flash': 'None',
                'acrobat': 'None',
                'reader': 'None',
                'java': 'None'
            }

            if not os.path.exists(file_path):
                print(f"❌ 找不到 {file_path}，跳過...")
                csv_writer.writerow([folder_name] + list(software_info.values()))
                continue

            print(f"✅ 解析 {file_path}...")

            with open(file_path, 'r', encoding='utf-16', errors='ignore') as log_file:
                lines = log_file.readlines()

                filter_conditions = {
                    'office': ['Microsoft Office Standard', 'Office 16 Click-to-Run', 
                               'Microsoft Office Professional Plus', 'Office 15 Click-to-Run'],
                    'flash': ['Adobe Flash'],
                    'reader': ['Adobe Acrobat Reader'],
                    'acrobat': ['Adobe Acrobat'],
                    'java': ['Java']
                }

                for line in lines:
                    clean_line = line.strip()
                    if clean_line and not clean_line.startswith('Caption'):
                        data = re.split(r'\s{2,}', clean_line)
                        if len(data) >= 5:
                            name = data[2].strip()
                            version = data[4].strip()
                            for key, conditions in filter_conditions.items():
                                if any(condition in name for condition in conditions):
                                    software_info[key] = f"{name} {version}"
                                    break

            csv_writer.writerow([folder_name] + list(software_info.values()))

    print(f"✅ 已生成 {office_csv_path}")

# 測試執行
# extract_software_data("data/檢視S", "data/檢視productlist_OFFICE")
