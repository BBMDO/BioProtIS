#change the path_root if necessary
#file align2d.py and model-single.py should in the main directory

import os
import shutil
from subprocess import call
path_root = "~/BioProtIS"
path_seqs = os.path.join(path_root, "Seqs")
path_docking = os.path.join(path_seqs, "Docking")
# Create the Docking folder inside Seqs.
os.makedirs(path_docking, exist_ok=True)
# Enter the Homology folder inside Seqs.
path_homology = os.path.join(path_seqs, "Homology")
os.chdir(path_homology)
# Iterate over all the folders inside Homology.
for folder in os.listdir():
    if not os.path.isdir(folder):
        continue
    
    # Enter the current folder.
    folder_path = os.path.join(path_homology, folder)
    os.chdir(folder_path)
    
    # Execute the align2d.py command.
    call(["python2", os.path.join(path_root, "align2d.py")], stdout=open("align2d.log", "w"))
    # Execute the model-single.py command.
    call(["python2", os.path.join(path_root, "model-single.py")], stdout=open("model-single.log", "w"))
    # Copy lines containing "model" and "pdb" to a new file.
    with open("model-single.log", "r") as log_file:
        lines = log_file.readlines()
        filtered_lines = [line for line in lines if "model" in line and "pdb" in line]
    # Sort the lines based on the third column (index 2).
    filtered_lines.sort(key=lambda line: float(line.split()[2]))
    with open("filtered_log.txt", "w") as filtered_log_file:
        filtered_log_file.writelines(filtered_lines)
    
    # Copy the best obtained model to the Docking folder.
    if filtered_lines:
        best_model = filtered_lines[0].split()[0]  # Get the value from the first row and first column.
        best_model_path = os.path.join(folder_path, best_model)
        docking_folder = os.path.join(path_docking, folder)
        os.makedirs(docking_folder, exist_ok=True)  # Create a folder with the name of the current folder in Docking.
        shutil.copy2(best_model_path, docking_folder)  # Copy the best model to the Docking folder.
    
    # Go back to the Homology folder.
    os.chdir(path_homology)
# Finish the code after going through all the folders inside Homology.
