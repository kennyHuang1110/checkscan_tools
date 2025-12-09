import csv
import re
import os


# ==========================================
# Office Version Classification
# ==========================================
def classify_office_version(ver):
    try:
        build = int(ver.split('.')[2])
    except:
        return "Unknown"

    if   4000  <= build < 10000:   return "Office 2016"
    elif 10000 <= build < 14000:   return "Office 2019"
    elif 14000 <= build < 15000:   return "Office 2021"
    elif 15000 <= build < 20000:   return "Microsoft 365"
    else: return "Unknown"


# ==========================================
# Main
# ==========================================
def extract_software_data(source_folder_path, target_folder_path):

    if not os.path.exists(target_folder_path):
        os.makedirs(target_folder_path)

    output_csv = os.path.join(target_folder_path, 'office.csv')

    folders = [
        name for name in os.listdir(source_folder_path)
        if os.path.isdir(os.path.join(source_folder_path, name))
    ]

    with open(output_csv, mode='w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)

        csv_writer.writerow([
            'HostName',
            'office_from_productlist',
            'office_from_clicktorun',
            'office_from_versionlog',
            'VersionNumber',
            'Office_Final',
            'Combined_Version',
            'Flash',
            'Acrobat',
            'Reader',
            'Java',
            'ClickToRun_ID'
        ])

        for folder in folders:

            pl_path  = os.path.join(source_folder_path, folder, 'productlist.log')
            ctr_path = os.path.join(source_folder_path, folder, 'ClickToRun.log')
            ver_path = os.path.join(source_folder_path, folder, 'officeversion.log')

            office_from_pl  = 'None'
            office_from_ctr = 'None'
            office_from_ver = 'None'
            version_number  = 'None'
            ctr_id = 'None'
            flash  = 'None'
            acrobat = 'None'
            reader = 'None'
            java   = 'None'

            # ========================
            # productlist.log
            # ========================
            if os.path.exists(pl_path):
                with open(pl_path, 'r', encoding='utf-16', errors='ignore') as f1:
                    for line in f1:
                        clean = line.strip()
                        if clean and not clean.startswith('Caption'):
                            arr = re.split(r'\s{2,}', clean)
                            if len(arr) >= 5:
                                name = arr[2].strip()
                                ver  = arr[4].strip()

                                # Office
                                if ('Microsoft Office' in name) or ('Office 16' in name):
                                    office_from_pl = ver

                                # Flash
                                elif 'Adobe Flash' in name:
                                    flash = ver

                                else:
                                    low = name.lower()

                                    # Reader
                                    if ('acrobat reader' in low) or ('adobe reader' in low):
                                        reader = f"{name} {ver}"

                                    # Acrobat full
                                    elif ('acrobat' in low) and ('reader' not in low):
                                        acrobat = f"{name} {ver}"

                                    # Java
                                    elif 'java' in low:
                                        java = ver


            # ========================
            # ClickToRun.log
            # ========================
            if os.path.exists(ctr_path):
                try:
                    lines = open(ctr_path, 'r', encoding='utf-16').readlines()
                except UnicodeError:
                    lines = open(ctr_path, 'r', encoding='utf-8', errors='ignore').readlines()

                for ln in lines:
                    if 'ProductReleaseIds' in ln:
                        m = re.search(r'ProductReleaseIds\s+\S+\s+(\S+)', ln)
                        if m:
                            ctr_id = m.group(1)
                            office_from_ctr = m.group(1)
                        break


            # ========================
            # officeversion.log
            # ========================
            if os.path.exists(ver_path):
                with open(ver_path, 'r', encoding='utf-8', errors='ignore') as f2:
                    text = f2.read()

                m = re.search(r'OFFICE_VER=(.*)', text)
                if m:
                    version_number = m.group(1).strip()

                    # 避免「假的 1.0.0.0」
                    if version_number == "1.0.0.0":
                        version_number = 'None'
                    else:
                        office_from_ver = classify_office_version(version_number)


            # =====================================================
            # FINAL DECISION （你要的最正確邏輯）
            # =====================================================

            # 1) 優先使用 productlist（只要有就永遠用它）
            if office_from_pl != "None" and re.match(r'\d+\.\d+\.\d+', office_from_pl):
                office_final = classify_office_version(office_from_pl)
                version_out = office_from_pl

            # 2) 次優使用 version_number
            elif version_number != "None" and re.match(r'\d+\.\d+\.\d+', version_number):
                office_final = classify_office_version(version_number)
                version_out = version_number

            # 3) 再來 CTR
            elif office_from_ctr != "None":
                office_final = office_from_ctr
                version_out = office_from_ctr

            # 4) 都沒有
            else:
                office_final = "None"
                version_out = "None"


            # =====================================================
            # Combined Output
            # =====================================================
            if office_final != "None" and version_out != "None":
                combined_version = f"{office_final}   {version_out}"
            elif office_final != "None":
                combined_version = office_final
            else:
                combined_version = "None"


            # ========================
            # Write CSV
            # ========================
            csv_writer.writerow([
                folder,
                office_from_pl,
                office_from_ctr,
                office_from_ver,
                version_number,
                office_final,
                combined_version,
                flash,
                acrobat,
                reader,
                java,
                ctr_id
            ])

    print(f"🔥 完成！輸出在: {output_csv}")
