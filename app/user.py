import os
import csv
import re

def read_file_multi_encoding(path):
    encodings = ['utf-16', 'utf-8', 'cp950', 'mbcs']
    for enc in encodings:
        try:
            return open(path, 'r', encoding=enc, errors='ignore').read().splitlines()
        except:
            pass
    return None


def extract_user_password(source_folder_path, target_folder_path):

    if not os.path.exists(target_folder_path):
        os.makedirs(target_folder_path)

    output_csv = os.path.join(target_folder_path, "user_password.csv")

    folder_names = [
        name for name in os.listdir(source_folder_path)
        if os.path.isdir(os.path.join(source_folder_path, name))
    ]

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['HostName', 'PasswDate'])

        for folder_name in folder_names:
            userpas_path = os.path.join(source_folder_path, folder_name, 'userpas.log')
            first_date = "None"

            print(f"[DEBUG] {folder_name}: Exists userpas.log? {os.path.exists(userpas_path)}")

            if os.path.exists(userpas_path):
                lines = read_file_multi_encoding(userpas_path)
                if lines:
                    for line in lines:
                        m = re.search(r'\d{4}/\d{1,2}/\d{1,2}', line)
                        if m:
                            first_date = m.group(0)
                            break

            writer.writerow([folder_name, first_date])

    print(f"\n🔥 完成！輸出位置: {output_csv}")
if __name__ == "__main__":
    src = r"data\檢視S"         # <<< 設你自己的路徑
    dst = r"data"              # <<< 設你自己的路徑

    extract_user_password(src, dst)