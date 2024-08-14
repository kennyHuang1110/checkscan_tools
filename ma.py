from app.unzip_tool import extract_rar_files
from app.productlist import convert_log_to_csv
from app.office_check import extract_office_data
from app.sysinfo import extract_system_info
from app.antivirus import extract_antivirus_data
from app.defender import extract_antivirus_and_hotfix_versions
from dotenv import load_dotenv
import pandas as pd
import os
# 載入.env文件
load_dotenv()

# 讀取.env文件中的變數
source_folder = os.getenv('SOURCE_FOLDER')
output_folder = os.getenv('OUTPUT_FOLDER')
password = os.getenv('PASSWORD')
product_folder_name = os.getenv('TARGET_FOLDER_NAME')
office_folder_name = os.getenv('TARGET2_FOLDER_NAME')
info_csv_name = os.getenv('TARGET3_CSV_NAME')
anti_folder_name= os.getenv("TARGET4_FOLDER_NAME")
defender_csv_name=os.getenv("TARGET5_CSV_NAME")
# ... and so on for other variables

def main():
    
    for folder in [output_folder, product_folder_name]:
        folder_path = os.path.join(source_folder, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"資料夾 {folder_path} 已創建")

    extract_rar_files(source_folder, output_folder, password)
    print("complete")

    parent_folder = os.path.dirname(output_folder)

    convert_log_to_csv(output_folder, os.path.join(parent_folder, product_folder_name))
    extract_office_data(output_folder, os.path.join(parent_folder, office_folder_name))
    extract_system_info(output_folder, os.path.join(parent_folder, info_csv_name))
    extract_antivirus_data(output_folder,os.path.join(parent_folder,anti_folder_name))
    extract_antivirus_and_hotfix_versions(output_folder,os.path.join(parent_folder,defender_csv_name))
if __name__ == "__main__":
    main()
# 讀取CSV檔案
df1 = pd.read_csv(r'檢視productlist_OFFICE\office.csv', encoding='utf-8')
df2 = pd.read_csv('檢視sysinfo.csv', encoding='utf-8')
df3 = pd.read_csv(r"檢視antivirus\antivirus.csv", encoding='utf-8')
df4 = pd.read_csv("Defender.csv",encoding="utf-8")
# 合併資料
merged_df = pd.merge(df1, df2, on='HostName', how='outer')
merged_df = pd.merge(merged_df, df3, on='HostName', how='outer')
merged_df = pd.merge(merged_df, df4, on='HostName', how='outer')

merged_df = merged_df.fillna('None')

# 將結果寫入CSV檔案
merged_df.to_csv('merged_data.csv', index=False, encoding='utf-8-sig')


