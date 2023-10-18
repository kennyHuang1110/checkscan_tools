import os
import csv

def extract_system_info(root_directory, output_csv_path):
    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['HostName', '作業系統', '作業系統版本'])

    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.endswith("systeminfo.log"):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r',) as file:
                    log_string = file.read()

                log_lines = log_string.split('\n')

                log_info = {
                    "HostName": None,
                    "作業系統": None,
                    "作業系統版本": None
                }

                for line in log_lines:
                    line_parts = line.split(': ')
                    if len(line_parts) == 2:
                        key, value = line_parts[0], line_parts[1].strip()
                        if key == '主機名稱':
                            log_info["HostName"] = value
                        elif key == '作業系統名稱':
                            log_info["作業系統"] = value
                        elif key == '作業系統版本':
                            version_parts = value.split(' ')
                            log_info["作業系統版本"] = version_parts[3]

                with open(output_csv_path, mode='a', newline='',encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([log_info["HostName"] if log_info["HostName"] else 'None', log_info["作業系統"] if log_info["作業系統"] else 'None', log_info["作業系統版本"] if log_info["作業系統版本"] else 'None'])
                
# if __name__ == "__main__":
#     root_directory = 
#     output_csv_path = 

#     extract_system_info(root_directory, output_csv_path)
