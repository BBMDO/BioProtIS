#change em.mdp if you desire
#change the path_root if necessary
#obabel command for the substrate."
#obabel -i sdf *.sdf -o pdbqt -O susbstrate.pdbqt --gen3D -p 7.4 --minimize --sd
#the susbstrate.pdbqt file should be in the path_root

###########
import os
path_root = "~/BioProtIS"
substrate_list_path = os.path.join(path_root, "substrate_list.txt") 

with open(substrate_list_path, "r") as substrate_file: 
    substrate_list = [line.strip() for line in substrate_file]

os.chdir(os.path.join(path_root, "Seqs", "Docking"))
# To enter each folder inside Docking
for folder_name in os.listdir():
    if os.path.isdir(folder_name):
        os.chdir(folder_name)
        # To create the 'tmp' folder and enter it
        os.makedirs("tmp", exist_ok=True)
        os.chdir("tmp")
        # To execute the command gmx pdb2gmx
        os.system("gmx pdb2gmx -f ../*.pdb -o protein_processed.gro -p protein.top -ff oplsaa -water tip4p")
        # To execute the command gmx editconf
        os.system("gmx editconf -f protein_processed.gro -o protein_box.gro -c -d 1.0 -bt cubic")
        # To execute the command gmx grompp
        os.system(f"gmx grompp -f {os.path.join(path_root, 'em.mdp')} -c protein_box.gro -p protein.top -o em.tpr")
        # To execute the command gmx mdrun
        os.system("gmx mdrun -v -s em.tpr -deffnm em -c em.pdb")
        # To execute the command obabel
        os.system("obabel -i pdb em.pdb -o pdb -O protein_no_spaces.pdb --centroid")
        # To execute the command fpocket
        os.system("sed -E 's/(\.[^ ]{3})/\1 /g' protein_no_spaces.pdb > protein_corr_no_spaces.pdb")
        os.system("fpocket -f protein_corr_no_spaces.pdb")
        os.system("sed '1,20d' protein_no_spaces_out/pockets/pocket1_atm.pdb > ../pocket1_atm.pdb ")
        # To execute the command sed
        os.system("sed '/CONECT/,$d' protein_corr_no_spaces.pdb > protein_no_spaces.pdbqt")
        os.system("sed -i '1,6d' protein_no_spaces.pdbqt")
        # To go back to the previous folder before 'tmp'
        os.chdir("..")
        #To move the file pocket1_atm.pdb
       # source_file = os.path.join(path_root, "Seqs", "Docking", folder_name, "tmp","protein_no_spaces_out","pockets", "pocket1_atm.pdb")
     #   destination_file = os.path.join(path_root, "Seqs", "Docking", folder_name, "pocket1_atm.pdb")
      #To move the file protein_no_spaces.pdbqt
        source_file = os.path.join(path_root, "Seqs", "Docking", folder_name, "tmp", "protein_no_spaces.pdbqt")
        destination_file = os.path.join(path_root, "Seqs", "Docking", folder_name, "protein_no_spaces.pdbqt")
        os.rename(source_file, destination_file)
        # To read the file protein_no_spaces.pdbq and calculate the values
        with open(os.path.join(path_root, "Seqs", "Docking", folder_name, "pocket1_atm.pdb")) as file:
            lines = file.readlines()
            column_6_values = [float(line.split()[5]) for line in lines if len(line.split()) >= 6]
            column_7_values = [float(line.split()[6]) for line in lines if len(line.split()) >= 7]
            column_8_values = [float(line.split()[7]) for line in lines if len(line.split()) >= 8]
        if column_6_values:
            x = max(column_6_values) - min(column_6_values)
            cx = x / 2
        else:
            x = cx = 0.1
        if column_7_values:
            y = max(column_7_values) - min(column_7_values)
            cy = y / 2
        else:
            y = cy = 0.1
        if column_8_values:
            z = max(column_8_values) - min(column_8_values)
            cz = z / 2
        else:
            z = cz = 0.1
        # Create the file conf.txt
        for substrate in substrate_list:
            with open(os.path.join(path_root, "Seqs", "Docking", folder_name, f"{substrate}_conf.txt"), "w") as file:
                file.write(f"receptor = protein_no_spaces.pdbqt\n")
                file.write(f"ligand = {os.path.join(path_root, substrate)}\n")
                file.write(f"out = {substrate}_poses.pdbqt\n")
                file.write("energy_range = 4\n")
                file.write("exhaustiveness = 50\n")
                file.write(f"center_x = {cx}\n")
                file.write(f"center_y = {cy}\n")
                file.write(f"center_z = {cz}\n")
                file.write(f"size_x = {x}\n")
                file.write(f"size_y = {y}\n")
                file.write(f"size_z = {z}\n")
        # To execute the command vina
            os.system(f"vina --config {os.path.join(path_root, 'Seqs', 'Docking', folder_name, f'{substrate}_conf.txt')} > {os.path.join(path_root, 'Seqs', 'Docking', folder_name, f'{substrate}_result_docking.txt')}")
        # To go back to the Docking folder
        os.chdir("..")
# To finalize the code
print("Docking Process Completed.")
