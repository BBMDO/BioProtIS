import os
import argparse
# Function to sort the lines by the value of the third column
def sort_lines_by_third_column(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
        lines.sort(key=lambda x: float(x.split()[2]), reverse=True)
    with open(filepath, 'w') as file:
        file.writelines(lines)
# Function to extract the second column from the first line and write it to "annotation.txt"
def extract_second_column(filepath):
    with open(filepath, 'r') as file:
        first_line = file.readline().split()[1]
        annotation = first_line
    folder_path = os.path.dirname(filepath)
    annotation_file = os.path.join(folder_path, "annotation.txt")
    with open(annotation_file, 'w') as file:
        file.write(annotation)
# Function to extract the first word before the underline in "annotation.txt" and write it to "pdb.txt"
def extract_first_word(filepath):
    folder_path = os.path.dirname(filepath)
    annotation_file = os.path.join(folder_path, "annotation.txt")
    with open(annotation_file, 'r') as file:
        first_word = file.readline().split('_')[0]
    pdb_file = os.path.join(folder_path, "pdb.txt")
    with open(pdb_file, 'w') as file:
        file.write(first_word)
# Function to process the Homology folder
def process_folder(folder, pipe):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.txt'):
                filepath = os.path.join(root, file)
                sort_lines_by_third_column(filepath)
                extract_second_column(filepath)
                extract_first_word(filepath)
                # Execute additional commands in the folder
                folder_path = os.path.dirname(filepath)
                # Command 1: seqtk subseq
                annotation_file_path = os.path.join(folder_path, "annotation.txt")
                command1 = f"seqtk subseq {pipe}/pdb_seqres.txt {annotation_file_path} > {folder_path}/template.fas"
                os.system(command1)
                # Command 2: batch_download.sh
                pdb_file_path = os.path.join(folder_path, "pdb.txt")
                command2 = f"{pipe}/batch_download.sh -f {folder_path}/pdb.txt -p && gunzip *.gz && mv *.pdb template.pdb && mv template.pdb {folder_path} && cp {folder_path}/*.fasta {folder_path}/model.fas"
                os.system(command2)
                # Command 3: fas_2_pir.sh for template.fas
                command3 = f"cd {folder_path} && {pipe}/fas_2_pir.sh template.fas"
                os.system(command3)
                # Command 4: fas_2_pir.sh for model.fas
                command4 = f"cd {folder_path} && {pipe}/fas_2_pir.sh model.fas"
                os.system(command4)
# Set up the argument parser
parser = argparse.ArgumentParser(description='Process text files in the Homology folder and perform additional steps.')

# Add an argument for the Homology folder location
parser.add_argument('-f', '--folder', type=str, help='Path to the Homology folder')
# Get the command line arguments
args = parser.parse_args()
# Check if the path is valid
if os.path.isdir(args.folder):
   #change the pipe if necessary
    pipe = "~/BioProtIS"  # Define the pipe path
    process_folder(args.folder, pipe)
    print("Processing completed.")
else:
    print("Invalid path.")
