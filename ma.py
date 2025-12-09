from app.unzip_tool import extract_rar_files
from app.productlist import convert_log_to_csv
from app.office_check import extract_software_data
from app.sysinfo import extract_system_info
from app.antivirus import extract_antivirus_data
from app.defender import extract_antivirus_and_hotfix_versions
from app.TCP_view import extract_tcpview_info
from app.user import extract_user_password

from dotenv import load_dotenv
import pandas as pd
import os

# 載入 .env 文件
load_dotenv()

# 設定變數
source_folder = os.getenv('SOURCE_FOLDER')
output_folder = os.getenv('OUTPUT_FOLDER')
password = os.getenv('PASSWORD')

product_folder_name = os.getenv('TARGET_FOLDER_NAME')  # 檢視productlist
office_folder_name = os.getenv('TARGET2_FOLDER_NAME')  # 檢視productlist_OFFICE
info_csv_name = os.getenv('TARGET3_CSV_NAME')  # 檢視sysinfo.csv
anti_folder_name = os.getenv("TARGET4_FOLDER_NAME")  # 檢視antivirus
defender_csv_name = os.getenv("TARGET5_CSV_NAME")  # Defender.csv

# 設定 `data` 為根目錄
parent_folder = "data"

# 確保 data 資料夾及其子資料夾存在
for folder in [output_folder, product_folder_name, office_folder_name, anti_folder_name]:
    print(repr(folder))
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"已創建資料夾: {folder}")

# 執行主要功能
def main():
    # extract_rar_files(source_folder, output_folder, password)
    print("解壓縮完成")

    convert_log_to_csv(output_folder, product_folder_name)
    extract_software_data(output_folder, office_folder_name)
    extract_system_info(output_folder, info_csv_name)  # **修正**
    extract_antivirus_data(output_folder, anti_folder_name)
    extract_antivirus_and_hotfix_versions(output_folder, defender_csv_name)
    extract_tcpview_info(output_folder, os.path.join(parent_folder, "tcp_suspicious_with_company.csv"))
    extract_user_password(output_folder, parent_folder)
    
if __name__ == "__main__":
    main()

# 讀取 CSV 檔案
df1_path = os.path.join("data\檢視productlist_OFFICE", "office.csv")
df2_path = os.path.join("data", "sysinfo.csv")
df3_path = os.path.join("data", "檢視antivirus", "antivirus.csv")
df4_path = os.path.join("data", "Defender.csv")
df5_path = os.path.join("data", "tcp_suspicious_with_company.csv")
df6_path = os.path.join("data", "user_password.csv")

# 確保所有 CSV 檔案存在，否則提示錯誤
for path in [df1_path, df2_path, df3_path, df4_path, df5_path, df6_path]:
    
    if not os.path.exists(path):
        print(f"錯誤: 找不到檔案 {path}")
    else:
        print(f"找到檔案: {path}")

# 確保所有檔案存在後才讀取
if all(os.path.exists(path) for path in [df1_path, df2_path, df3_path, df4_path,df5_path,df6_path]):
    df1 = pd.read_csv(df1_path, encoding='utf-8')
    df2 = pd.read_csv(df2_path, encoding='utf-8')
    df3 = pd.read_csv(df3_path, encoding='utf-8')
    df4 = pd.read_csv(df4_path, encoding="utf-8")
    df5 = pd.read_csv(df5_path, encoding="utf-8")
    df6 = pd.read_csv(df6_path, encoding="utf-8")
   

    # 合併資料
    merged_df = pd.merge(df1, df2, on='HostName', how='outer')
    merged_df = pd.merge(merged_df, df3, on='HostName', how='outer')
    merged_df = pd.merge(merged_df, df4, on='HostName', how='outer')
    merged_df = pd.merge(merged_df, df5, on='HostName', how='outer')
    merged_df = pd.merge(merged_df, df6, on='HostName', how='outer')



    # 填補缺失值
    merged_df = merged_df.fillna('None')

    # 將結果寫入 CSV
    merged_output_path = os.path.join("data", "merged_data.csv")
    merged_df.to_csv(merged_output_path, index=False, encoding='utf-8-sig')
    print(f"合併完成: {merged_output_path}")
