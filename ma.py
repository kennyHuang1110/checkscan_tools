from app.unzip_tool import extract_rar_files
from app.productlist import convert_log_to_csv
from app.productlist_audit import main as run_productlist_audit
from app.office_check import extract_software_data
from app.sysinfo import extract_system_info
from app.antivirus import extract_antivirus_data
from app.defender import extract_antivirus_and_hotfix_versions
from app.TCP_view import extract_tcpview_info
from app.user import extract_user_password

from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import os

load_dotenv()

source_folder = os.getenv('SOURCE_FOLDER')
output_folder = os.getenv('OUTPUT_FOLDER')
password = os.getenv('PASSWORD')

product_folder_name = os.getenv('TARGET_FOLDER_NAME')
office_folder_name = os.getenv('TARGET2_FOLDER_NAME')
info_csv_name = os.getenv('TARGET3_CSV_NAME')
anti_folder_name = os.getenv('TARGET4_FOLDER_NAME')
defender_csv_name = os.getenv('TARGET5_CSV_NAME')

parent_folder = 'data'

for folder in [output_folder, product_folder_name, office_folder_name, anti_folder_name]:
    print(repr(folder))
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
        print(f'建立資料夾: {folder}')


def main():
    extract_rar_files(source_folder, output_folder, password)
    print('解壓完成')

    convert_log_to_csv(output_folder, product_folder_name)
    run_productlist_audit(Path(product_folder_name), Path(parent_folder) / 'productlist_legacy_report.csv')

    extract_software_data(output_folder, office_folder_name)
    extract_system_info(output_folder, info_csv_name)
    extract_antivirus_data(output_folder, anti_folder_name)
    extract_antivirus_and_hotfix_versions(output_folder, defender_csv_name)
    extract_tcpview_info(output_folder, os.path.join(parent_folder, 'tcp_suspicious_with_company.csv'))
    extract_user_password(output_folder, parent_folder)


if __name__ == '__main__':
    main()


df1_path = os.path.join('data\\檢視productlist_OFFICE', 'office.csv')
df2_path = os.path.join('data', 'sysinfo.csv')
df3_path = os.path.join('data', '檢視antivirus', 'antivirus.csv')
df4_path = os.path.join('data', 'Defender.csv')
df5_path = os.path.join('data', 'tcp_suspicious_with_company.csv')
df6_path = os.path.join('data', 'user_password.csv')
df7_path = os.path.join('data', 'productlist_legacy_report.csv')

for path in [df1_path, df2_path, df3_path, df4_path, df5_path, df6_path, df7_path]:
    if not os.path.exists(path):
        print(f'找不到檔案: {path}')
    else:
        print(f'已找到檔案: {path}')

if all(os.path.exists(path) for path in [df1_path, df2_path, df3_path, df4_path, df5_path, df6_path, df7_path]):
    df1 = pd.read_csv(df1_path, encoding='utf-8')
    df2 = pd.read_csv(df2_path, encoding='utf-8')
    df3 = pd.read_csv(df3_path, encoding='utf-8')
    df4 = pd.read_csv(df4_path, encoding='utf-8')
    df5 = pd.read_csv(df5_path, encoding='utf-8')
    df6 = pd.read_csv(df6_path, encoding='utf-8')
    df7 = pd.read_csv(df7_path, encoding='utf-8')

    merged_df = pd.merge(df2, df1, on='HostName', how='outer')
    merged_df = pd.merge(merged_df, df3, on='HostName', how='outer')
    merged_df = pd.merge(merged_df, df4, on='HostName', how='outer')
    merged_df = pd.merge(merged_df, df5, on='HostName', how='outer')
    merged_df = pd.merge(merged_df, df6, on='HostName', how='outer')
    merged_df = pd.merge(merged_df, df7, on='HostName', how='outer')

    merged_df = merged_df.fillna('None')

    merged_output_path = os.path.join('data', 'merged_data.csv')
    merged_df.to_csv(merged_output_path, index=False, encoding='utf-8-sig')
    print(f'合併輸出: {merged_output_path}')
