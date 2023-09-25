#change the path_root if necessary

import os
import shutil
import csv
import matplotlib.pyplot as plt
# Set the path_root
path_root = '.'
# Enter the folder path_root/Seqs/Docking
path_docking = os.path.join(path_root, 'Seqs', 'Docking')
os.chdir(path_docking)
# Create a list to store the results.
docking_results = []
# Iterate through all the folders within the Docking folder.
for folder_name in os.listdir():
    folder_path = os.path.join(path_docking, folder_name)
    
    if os.path.isdir(folder_path):
        os.chdir(folder_path)
        
        # Find all files with the suffix "result_docking.txt"
        result_files = [file for file in os.listdir() if file.endswith("result_docking.txt")]
        prefix = ""        
        # Iterate through all found result files
        for result_file_name in result_files:
            with open(result_file_name, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 40:
                    line_parts = lines[39].split()
                    if len(line_parts) >= 2:
                        energy_value = line_parts[1]
                        prefix = result_file_name.replace("_result_docking.txt", "").replace(".pdbqt", "")  # Extract prefix
                        docking_results.append((folder_name, prefix, energy_value))
                
                # Save the value in a file named best_energy.txt.
                best_energy_file = result_file_name.replace("result_docking.txt", "best_energy.txt")
                with open(best_energy_file, 'w') as file:
                    file.write(str(energy_value))
        
        os.chdir(path_docking)
# Create a file named docking_results.txt containing the values from best_energy.txt.
with open('docking_results.txt', 'w') as file:
    for folder_name, prefix, energy_value in docking_results:
        file.write(f"{folder_name}\t{prefix}\t{energy_value}\n")
# Remove the lines that contain empty columns in the docking_results.txt file.
with open('docking_results.txt', 'r') as file:
    lines = file.readlines()
    lines = [line for line in lines if line.strip()]
    
with open('docking_results.txt', 'w') as file:
    file.writelines(lines)
# Update the docking_results.txt file with the third column.
with open("docking_results.txt", "r") as file_docking_results:
    reader = csv.reader(file_docking_results, delimiter="\t")
    updated_docking_results = []
    for row in reader:
        folder_name = row[0]
        prefix = row[1].replace(".pdbqt", "")
        seq_path = os.path.join(path_root, "Seqs", folder_name)
        output_file_path = os.path.join(seq_path, folder_name + ".output.txt")
        with open(output_file_path, "r") as output_file:
            first_line = output_file.readline().strip()
            updated_row = row + [first_line]
            updated_docking_results.append(updated_row)
with open("docking_results.txt", "w") as file_docking_results:
    writer = csv.writer(file_docking_results, delimiter="\t")
    writer.writerow(["Directory", "Substrate", "Best Energy", "Docking Annotation"])
    writer.writerows(updated_docking_results)
# Rename the file docking_results.txt to docking_results_final.txt.
shutil.move(
    os.path.join(path_docking, "docking_results.txt"),
    os.path.join(path_docking, "docking_results_final.txt")
)
# Finish the code.
print("Code successfully completed.")
