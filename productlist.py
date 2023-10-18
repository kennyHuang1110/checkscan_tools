import csv
import re
import os

def convert_log_to_csv(source_folder_path, target_folder_name):
    target_folder_path = os.path.join(source_folder_path, target_folder_name)

    if not os.path.exists(target_folder_path):
        os.makedirs(target_folder_path)

    folder_names = [name for name in os.listdir(source_folder_path) if os.path.isdir(os.path.join(source_folder_path, name))]

    for folder_name in folder_names:
        file_path = os.path.join(source_folder_path, folder_name, 'productlist.log')
        csv_file_name = folder_name + '.csv'
        target_csv_path = os.path.join(target_folder_path, csv_file_name)

        if not os.path.exists(file_path):
            with open(target_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Caption', 'IdentifyingNumber', 'Name', 'Vendor', 'Version'])
                csv_writer.writerow(['None', 'None', 'None', 'None', 'None'])
            print(f"找不到 productlist.log，已生成 'None'。")
            continue

        with open(file_path, 'r', encoding='utf-16') as log_file:
            lines = log_file.readlines()

        with open(target_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Caption', 'IdentifyingNumber', 'Name', 'Vendor', 'Version'])
            for line in lines:
                clean_line = line.strip()
                if clean_line and not clean_line.startswith('Caption'):
                    data = re.split(r'\s{2,}', clean_line)
                    if len(data) >= 5:
                        caption = data[0].strip()
                        identifying_number = data[1].strip()
                        name = data[2].strip()
                        vendor = data[3].strip()
                        version = data[4].strip()
                        csv_writer.writerow([caption, identifying_number, name, vendor, version])
                    else:
                        print(f"無法處理的行內容為: {clean_line}")

        print(f"{target_csv_path} 文件已生成。")

# if __name__ == "__main__":
#     source_folder_path = 
#     target_folder_name = 

#     convert_log_to_csv(source_folder_path, target_folder_name)
