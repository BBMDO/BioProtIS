#change the path_root if necessary
#file align2d.py and model-single.py should in the main directory

import os
import shutil
from subprocess import call
import subprocess

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
    
    # Execute alphafold
    import subprocess

    command = [
        "python3",
        "docker/run_docker.py",
        "--fasta_paths=T1050.fasta",
        "--max_template_date=2020-05-14",
        "--model_preset=monomer",
        "--db_preset=reduced_dbs",
        f"--data_dir={DOWNLOAD_DIR}",
        "--output_dir=/home/user/absolute_path_to_the_output_dir"
    ]

    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
  
    # Copy the best obtained model to the Docking folder.
    source_folder = os.path.join(folder_path)
    docking_folder = os.path.join(path_docking, folder)
    os.makedirs(docking_folder, exist_ok=True)  # Create a folder with the name of the current folder in Docking.
    shutil.copy2(os.path.join(source_folder, "ranked_0.pdb"), docking_folder)
    # Go back to the Homology folder.
    os.chdir(path_homology)
# Finish the code after going through all the folders inside Homology.
