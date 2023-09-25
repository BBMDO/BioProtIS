# BioProtIS

# BioProtIS -  Bioprospecting Proteins through Inverse Virtual Screening

BioProtIS is an innovative computational pipeline designed for the automated analysis of protein-ligand interactions at a genomic and transcriptomic scale. This tool leverages a range of cutting-edge software, including Modeller, AlphaFold, GROMACS, FPOCKET, and AutoDock Vina, to enable efficient and precise ligand docking with a wide array of proteins and substrates. BioProtIS offers versatility, accommodating various testing scenarios, from blind docking to site-specific targeting, making it valuable for drug discovery, allosteric binding site exploration, and toxicity assessments. The pipeline is highly modular, allowing users to customize it to their research needs, and it promises ongoing advancements in the field of computational biology by facilitating the integration of additional docking algorithms.

* **Software Required:**
    + Python 3.10 or higher
        <ul> packages
            <li>`os`,`shutil`,`subprocess,`csv`,`matplotlib.pyplot,`re`,`openai`, and `argparse`.</li>
        </ul>
    + Python 2
    + Modeller (https://www.gnu.org/software/parallel/)
    + AlphaFold (https://github.com/google-deepmind/alphafold.git)
    + BLAST (sudo apt-get install ncbi-blast+)
    + GROMACS (sudo apt-get install gromacs)
    + Seqtk (sudo apt-get install seqtk)
    + FPOCKET (https://github.com/Discngine/fpocket.git or via conda)
    + Autodock Vina (http://vina.scripps.edu/)
    + #batch_download.sh
      wget https://www.rcsb.org/scripts/batch_download.sh
      chmod +x batch_download.sh
    + PDB local database
      wget https://ftp.wwpdb.org/pub/pdb/derived_data/pdb_seqres.txt.gz
      gunzip pdb_seqres.txt.gz
      sed -i 's/ /_/g' pdb_seqres.txt
      mkdir db
      makeblastdb -in pdb_seqres.txt -dbtype prot -out db/db
 
  * **BioProtIS Installation:**
      + No installation is needed. Simply unzip and use the scripts, providing the directory path in the scripts.
  
  * **Scripts description:**
      + Step1 - fasta_file_processing.py
        Description:
        This Python script performs several tasks for processing FASTA files. It reads an input FASTA file containing amino acid sequences, creates a 'Seqs' folder, separates the input file into individual files, changes their headers, executes a blastp command within the folders, and manages the organization of files into different folders based on specific criteria. This script is designed to automate and streamline the initial steps of sequence analysis and homology search.
   
      + Step2 - homology_folder_processing.py
        Description:
        This Python script processes text files within the Homology folder and performs additional steps. It sorts the lines in these text files by the value of the third column, extracts information from these files, executes additional commands in the folder, and prepares data for further analysis. This script streamlines the processing of data related to homology and sequence comparisons.
   
      + Step 3a (Using modeller) - modeller_homology.py
        Description:
        This Python script is designed to process data within the Homology folder of the BioProtIS project. It assumes that the `align2d.py` and `model-single.py` files are located in the main directory. The script performs various tasks, including executing these two Python scripts, sorting and filtering log files, and organizing resulting files into specific folders. It is a useful tool for managing and analyzing data in the context of protein structure prediction and homology modeling.
   
      + Step 3b (Using AlphaFold) - alphafold_homology.py
        Description:
        This Python script is designed to process data within the Homology folder of the BioProtIS project. It assumes that the AlphaFold model is used for protein structure prediction and that the required files are in place. The script executes the AlphaFold command for each folder, generates protein structure models, and copies the best model to the Docking folder for further analysis. It is a useful tool for managing and analyzing protein structure prediction data.
   
      + Step 4a -  blind_docking.py
        Description:
        This Python script automates blind molecular docking simulations for a list of substrates using the AutoDock Vina software. It prepares protein structures, calculates docking parameters, and executes the docking simulations, saving the results in an organized manner. The script is highly configurable, allowing you to specify various parameters such as energy range, exhaustiveness, and more.
   
      +  Step 4b - pocket_docking.py
        Description:
        This Python script automates pocket molecular docking simulations using AutoDock Vina, while also performing preliminary analysis of substrates. It prepares protein structures, calculates docking parameters, and executes the docking simulations. Additionally, it analyzes substrate properties and generates configuration files for docking. The script provides flexibility to customize parameters such as energy range and exhaustiveness. It is designed to streamline the process of molecular docking with a focus on substrate analysis, making it a valuable tool for computational biology and drug discovery research.
   
      +  Step 5 -  results_aggregator.py
      +  Description:
      +   This Python script automates the aggregation and analysis of molecular docking results. It navigates through a directory structure, extracts energy values, and creates a structured output file named "docking_results_final.txt." The script also associates additional information, such as docking annotations, with each result. The generated output facilitates the comprehensive analysis and visualization of molecular docking experiments, making it a valuable tool for researchers in computational biology and drug discovery.
   
**Usage:**
python fasta_file_processing.py input.fas
python homology_folder_processing.py -f Seqs/Homology/
python modeller_homology.py or python alphafold_homology.py
python blind_docking.py or python pocket_docking.py
   
**Included a document called substrate_list.txt, containing the list of substrates:**
python results_aggregator.py
Version v1.0

