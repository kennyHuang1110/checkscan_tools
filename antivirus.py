import csv
import re
import os

def extract_antivirus_data(source_folder_path, target_folder_name):
    # 目標資料夾路徑
    target_folder_path = os.path.join(source_folder_path, target_folder_name)

    # 如果目標資料夾不存在則創建
    if not os.path.exists(target_folder_path):
        os.makedirs(target_folder_path)

    # 獲取所有資料夾名稱
    folder_names = [name for name in os.listdir(source_folder_path) if os.path.isdir(os.path.join(source_folder_path, name))]

    # 建立並寫入 CSV 檔案
    with open(os.path.join(target_folder_path, 'antivirus.csv'), mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['HostName', 'antivirus_version'])

        for folder_name in folder_names:
            file_path_productlist = os.path.join(source_folder_path, folder_name, 'productlist.log')
            file_path_windowsupdate = os.path.join(source_folder_path, folder_name, 'WindowsUpdateListhtml.log')

            # 如果 productlist.log 檔案存在，則處理它
            if os.path.exists(file_path_productlist):
                with open(file_path_productlist, 'r', encoding='utf-16') as log_file:
                    lines = log_file.readlines()

                    antivirus_info = None
                    # 過濾條件列表
                    filter_conditions = [
                        "Trend Micro",
                        'OfficeScan',
                        'Azure Advanced Threat',
                        'Security',
                        "卡巴斯基",
                        "McAfee",
                        "ESET",
                        "F-Secure",
                        "Avira",
                        "Avast"
                    ]

                    # 解析日誌檔案並匹配相應的資訊
                    for line in lines:
                        clean_line = line.strip()
                        if clean_line and not clean_line.startswith('Caption'):
                            data = re.split(r'\s{2,}', clean_line)
                            if len(data) >= 5:
                                name = data[2].strip()
                                version = data[4].strip()
                                for condition in filter_conditions:
                                    if condition in name:
                                        antivirus_info = f"{name} {version}"
                                        break
                                else:
                                    continue
                                break
                    # 寫入CSV文件
                    csv_writer.writerow([folder_name, antivirus_info if antivirus_info else 'None'])

            # 如果 productlist.log 檔案不存在或沒有相關資訊，則處理 WindowsUpdateListhtml.log 檔案
            elif os.path.exists(file_path_windowsupdate):
                with open(file_path_windowsupdate, 'r', encoding='latien-1') as log_file:
                    lines = log_file.readlines()

                    for line in lines:
                        match = re.search(r'Microsoft Defender Antivirus\s*(版本\s*\d+\.\d+\.\d+\.\d+)', line)
                        if match:
                            antivirus_info = match.group(1)
                            break
                    else:
                        antivirus_info = 'None'
                    # 寫入CSV文件
                    csv_writer.writerow([folder_name, antivirus_info])

            # 如果兩個檔案都不存在，則寫入'None'
            else:
                csv_writer.writerow([folder_name, 'None'])

    # 印出訊息
    print(f"已生成 {target_folder_name}/antivirus.csv 檔。")
