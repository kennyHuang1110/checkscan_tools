import csv
import re
import os
from bs4 import BeautifulSoup

def extract_antivirus_data(source_folder_path, target_folder_path):
    """
    從 productlist.log 和 WindowsUpdateListhtml.log 提取防毒軟體資訊，存為 antivirus.csv。

    :param source_folder_path: 來源資料夾 (通常為 data/檢視S)
    :param target_folder_path: 儲存目標資料夾 (通常為 data/檢視antivirus)
    """
    # 確保目標資料夾存在
    if not os.path.exists(target_folder_path):
        os.makedirs(target_folder_path)
        print(f"📂 目標資料夾已創建: {target_folder_path}")

    # 設定 CSV 檔案路徑
    antivirus_csv_path = os.path.join(target_folder_path, 'antivirus.csv')

    # 讀取 source_folder_path 內的所有子資料夾
    folder_names = [name for name in os.listdir(source_folder_path) if os.path.isdir(os.path.join(source_folder_path, name))]

    with open(antivirus_csv_path, mode='w', newline='', encoding='utf-8', errors='replace') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['HostName', 'antivirus_version'])

        for folder_name in folder_names:
            antivirus_info = None  # 預設為 None
            file_path_productlist = os.path.join(source_folder_path, folder_name, 'productlist.log')
            file_path_windowsupdate = os.path.join(source_folder_path, folder_name, 'WindowsUpdateListhtml.log')

            # 解析 productlist.log
            if os.path.exists(file_path_productlist):
                print(f"✅ 解析 {file_path_productlist}...")
                with open(file_path_productlist, 'r', encoding='utf-16', errors='ignore') as log_file:
                    lines = log_file.readlines()

                    filter_conditions = [
                        "Trend Micro", "OfficeScan", "Azure Advanced Threat", 
                        "Kaspersky Endpoint", "McAfee", "ESET", "F-Secure", 
                        "Avira", "Avast", "Xcitium", "COMODO", "Symantec", 
                        "Sophos Endpoint", "Trellix", "ahnLab","PC-cillin"
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
                                        antivirus_info = f"{name} {version}"
                                        break
                                else:
                                    continue
                                break

            # 解析 WindowsUpdateListhtml.log
            if antivirus_info is None and os.path.exists(file_path_windowsupdate):
                print(f"✅ 解析 {file_path_windowsupdate}...")
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
                                        antivirus_info = f"Microsoft Defender Antivirus {version_match.group(0)}"
                                        break

            # 若無任何資訊，則填入 'None'
            if antivirus_info is None:
                print(f"⚠️ {folder_name} 沒有找到防毒軟體資訊，填入 'None'。")
                antivirus_info = 'None'

            # 寫入 CSV
            csv_writer.writerow([folder_name, antivirus_info])

    print(f"✅ 已生成 {antivirus_csv_path}")
