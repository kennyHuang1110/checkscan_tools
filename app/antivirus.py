import csv
import re
import os
from bs4 import BeautifulSoup

def extract_antivirus_data(source_folder_path, target_folder_name):
    # 目標資料夾路徑
    target_folder_path = os.path.join(source_folder_path, target_folder_name)

    # 如果目標資料夾不存在則創建
    if not os.path.exists(target_folder_path):
        os.makedirs(target_folder_path)

    # 獲取所有資料夾名稱
    folder_names = [name for name in os.listdir(source_folder_path) if os.path.isdir(os.path.join(source_folder_path, name))]

    # 建立並寫入 CSV 檔案
    antivirus_csv_path = os.path.join(target_folder_path, 'antivirus.csv')
    with open(antivirus_csv_path, mode='w', newline='', encoding='utf-8', errors='replace') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['HostName', 'antivirus_version'])

        for folder_name in folder_names:
            antivirus_info = None
            file_path_productlist = os.path.join(source_folder_path, folder_name, 'productlist.log')
            file_path_windowsupdate = os.path.join(source_folder_path, folder_name, 'WindowsUpdateListhtml.log')

            # 如果 productlist.log 檔案存在，則處理它
            if os.path.exists(file_path_productlist):
                with open(file_path_productlist, 'r', encoding='utf-16', errors='ignore') as log_file:
                    lines = log_file.readlines()

                    # 過濾條件列表
                    filter_conditions = [
                        "Trend Micro",
                        'OfficeScan',
                        'Azure Advanced Threat',
                        'WithSecure',
                        "卡巴斯基",
                        "McAfee",
                        "ESET",
                        "F-Secure",
                        "Avira",
                        "Avast",
                        'Xcitium',
                        "COMODO",
                        "Symantec",
                        "Sophos Endpoint"
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
                with open(file_path_windowsupdate, 'r', encoding="utf-8", errors='ignore') as log_file:
                    html_content = log_file.read()

                    soup = BeautifulSoup(html_content, "html.parser")
                    table = soup.find("table")

                    if table:
                        for row in table.find_all("tr"):
                            cells = row.find_all("td")
                            if cells:
                                name = cells[0].text.strip()
                                description = cells[1].text.strip()

                                if "Microsoft Defender Antivirus" in name:
                                    version_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', description)
                                    if version_match:
                                        first_version = version_match.group(0)
                                        antivirus_info = f"Microsoft Defender Antivirus {first_version}"
                                        break

                    if not antivirus_info:
                        antivirus_info = 'None'

                    # 寫入CSV文件
                    csv_writer.writerow([folder_name, antivirus_info])

            # 如果兩個檔案都不存在，則寫入'None'
            else:
                csv_writer.writerow([folder_name, 'None'])

    # 印出訊息
    print(f"已生成 {antivirus_csv_path} 檔。")

