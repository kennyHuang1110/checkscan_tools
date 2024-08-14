import os
import csv
import patoolib
import rarfile

def extract_rar_files(source_folder, output_folder, password):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for rar_filename in os.listdir(source_folder):
        if rar_filename.endswith('.rar'):
            # Create the corresponding directory
            directory_name = os.path.splitext(rar_filename)[0]
            directory_path = os.path.join(output_folder, directory_name)
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

            # Extract the RAR files
            cmd = f'unrar x -p{password} "{os.path.join(source_folder, rar_filename)}" "{directory_path}"'
            os.system(cmd)

# if __name__ == "__main__":
#     source_folder = 
#     output_folder = 
#     password = 
    
#     extract_rar_files(source_folder, output_folder, password)
#     print("complete")
