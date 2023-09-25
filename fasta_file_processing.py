import os
import sys
import shutil
import subprocess

#change the path_root if necessary
root = "~/BioProtIS"

# Function to read the input file containing the amino acid sequence.
def read_input_file(file_name):
    try:
        with open(file_name, 'r') as file:
            sequence = file.read()
        return sequence
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        sys.exit(1)

# Function to create the 'Seqs' folder.
def create_folder_seq():
    try:
        os.mkdir('Seqs')
        print("Folder 'Seqs' created successfully.")
    except FileExistsError:
        print("Folder 'Seqs' already exist.")

# Function to change the header of the FASTA file to the file name.
def change_header_file(file_name):
    file_name_output = 'Seqs/' + os.path.basename(file_name)
    file_name_output = file_name_output.replace('.fasta', '')
    with open(file_name_output, 'w') as file_output:
        file_output.write(f">{file_name_output}\n" + sequence)
    print(f"file '{file_name_output}' created successfully.")

# Function to separate the FASTA file into individual files.
def separate_file_fasta(file_name):
    with open(file_name, 'r') as file_input:
        content = file_input.read()
    sequences = content.split('\n>')

    for i, sequence in enumerate(sequences):
        file_name_output = f"Seqs/T{i+1}.fasta"
        with open(file_name_output, 'w') as file_output:
            file_output.write(f">{sequence}")
        print(f"file '{file_name_output}' created successfully.")

# Function to create individual folders for each FASTA file.
def create_individual_folder():
    for file in os.listdir('Seqs'):
        if file.endswith(".fasta"):
            name_folder = os.path.splitext(file)[0]
            os.makedirs(f"Seqs/{name_folder}", exist_ok=True)
            print(f"Folder'{name_folder}' created successfully.")

# Function to move the FASTA files to their respective folders.
def move_files_to_folders():
    for file in os.listdir('Seqs'):
        if file.endswith(".fasta"):
            name_folder = os.path.splitext(file)[0]
            shutil.move(f"Seqs/{file}", f"Seqs/{name_folder}/{file}")

# Function to execute the blastp command within the folders.
def execute_command_blastp():
    for folder in os.listdir('Seqs'):
        complete_folder = os.path.join('Seqs', folder)
        if os.path.isdir(complete_folder):
            command = f"blastp -db {root}/db/db -query {complete_folder}/* -evalue 1e-10 -max_target_seqs 5 -out {root}/Seqs/{folder}/{folder}.output.txt -outfmt '6 qseqid stitle pident qcovs length mismatch gapopen evalue bitscore'"
            subprocess.run(command, shell=True)
            print(f"Blastp command executed in the folder '{folder}'.")

# Function to create the 'non_annotate' folder
def create_folder_non_annotate():
    try:
        os.mkdir('Seqs/non_annotate')
        print("folder 'non_annotate' created successfully.")
    except FileExistsError:
        print("Folder 'non_annotate' already exist.")

# Function to move folders with empty 'output.txt' files to the 'non_annotate' folder.
def move_folders_empty():
    for folder in os.listdir('Seqs'):
        complete_folder = os.path.join('Seqs', folder)
        if os.path.isdir(complete_folder):
            files_output = os.listdir(complete_folder)
            for file in files_output:
                if file.endswith(".output.txt"):
                    file_complete = os.path.join(complete_folder, file)
                    if os.path.getsize(file_complete) == 0:
                        shutil.move(complete_folder, f"Seqs/non_annotate/{folder}")
                        print(f"folder '{folder}' moved to 'non_annotate'.")
                        
# Function to create the 'Homology' folder.
def create_folder_homology():
    try:
        os.mkdir('Seqs/Homology')
        print("folder 'Homology' created successfully.")
    except FileExistsError:
        print("Folder 'Homology' already exist.")

# Function to copy folders with a value greater than 50 in the third column of the 'output.txt' file to the 'Homology' folder.
def copy_folders_value_greater_50():
    for folder in os.listdir('Seqs'):
        complete_folder = os.path.join('Seqs', folder)
        if os.path.isdir(complete_folder) and folder.startswith('T'):
            files_output = os.listdir(complete_folder)
            for file in files_output:
                if file.endswith(".output.txt"):
                    file_complete = os.path.join(complete_folder, file)
                    with open(file_complete, 'r') as file_output:
                        for line in file_output:
                            values = line.split('\t')
                            if len(values) >= 3:
                                value_column_3 = float(values[2])
                                if value_column_3 > 50:
                                    destine = os.path.join('Seqs/Homology/',folder)
                                    os.makedirs(destine, exist_ok=True)
                                    for item in os.listdir(complete_folder):
                                        origem = os.path.join(complete_folder, item)
                                        shutil.copy2(origem, destine)
                                    print(f"Folder '{folder}' copied to 'Homology'.")

# Get the name of the input file passed as an argument from the command line.
file_name_input = sys.argv[1]

# Reading the input file.
sequence = read_input_file(file_name_input)

# Creating the 'Seqs' folder.
create_folder_seq()

# Changing the header of the FASTA file to the name of the file.
change_header_file(file_name_input)

# Separating the FASTA file into individual files.
separate_file_fasta(file_name_input)

# Creating individual folders for each fasta file.
create_individual_folder()

# Moving the fasta files to their respective folders.
move_files_to_folders()

# Executing the blastp command within the folders.
execute_command_blastp()

# Creating the 'non_annotate' folder.
create_folder_non_annotate()

# Moving folders with empty 'output.txt' files to the 'non_annotate' folder.
move_folders_empty()

# Criação da folder 'Homology'
create_folder_homology()

# Copying folders with a value greater than 50 in the third column of the 'saida.txt' file to the 'Homology' folder.
copy_folders_value_greater_50()
