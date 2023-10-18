from unzip_tool import extract_rar_files
from productlist import convert_log_to_csv
from office_check import extract_office_data
from sysinfo import extract_system_info
from dotenv import load_dotenv
import os
# 載入.env文件
load_dotenv()

# 讀取.env文件中的變數
source_folder = os.getenv('SOURCE_FOLDER')
output_folder = os.getenv('OUTPUT_FOLDER')
password = os.getenv('PASSWORD')
target_folder_name = os.getenv('TARGET_FOLDER_NAME')
target2_folder_name = os.getenv('TARGET2_FOLDER_NAME')
target3_csv_name = os.getenv('TARGET3_CSV_NAME')


def main():
    for folder in [output_folder, target_folder_name, target2_folder_name]:
        folder_path = os.path.join(source_folder, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"資料夾 {folder_path} 已創建")

    extract_rar_files(source_folder, output_folder, password)
    print("complete")

    parent_folder = os.path.dirname(output_folder)

    convert_log_to_csv(output_folder, os.path.join(parent_folder, target_folder_name))
    extract_office_data(output_folder, os.path.join(parent_folder, target2_folder_name))
    extract_system_info(output_folder, os.path.join(parent_folder, target3_csv_name))

if __name__ == "__main__":
    main()
