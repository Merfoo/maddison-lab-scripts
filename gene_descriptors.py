# Produces files for relationships between sequences and primers
import os
import re
import csv
import argparse

def get_primers(primers_file_path):
    primers = {}

    with open(primers_file_path, "rb") as csv_file:
        primers_reader = csv.reader(csv_file, delimiter="\t")

        for row in primers_reader:
            name = row[0]

            if name:
                primers[name.upper()] = { "gene_name": row[1], "type": row[2] }

    return primers
    
def get_chromatogram_filenames(chromatograms_folder_path):
    chromatogram_filenames = {}

    for chromatogram_filename in os.listdir(chromatograms_folder_path):
        if chromatogram_filename[0] == ".":
            continue

        dna_number = get_chromatogram_dna_number(chromatogram_filename)

        if not chromatogram_filenames.has_key(dna_number):
            chromatogram_filenames[dna_number] = []

        chromatogram_filenames[dna_number].append(chromatogram_filename)

    return chromatogram_filenames

def get_chromatogram_dna_number(chromatogram_filename):
    # Example chromatogram filename
    # A10_DNA2124_LC1490_1800817_080.ab1
    dna_number_match = re.search("DNA(?P<dna_number>\d+)", chromatogram_filename)

    if dna_number_match:
        return dna_number_match.group("dna_number")
    else:
        return None

def get_chromatogram_primer(chromatogram_filename):
    # Example chromatogram filename
    # A10_DNA2124_LC1490_1800817_080.ab1
    primer_name_match = re.search("_.+?_(?P<primer_name>.+?)_", chromatogram_filename)

    if primer_name_match:
        return primer_name_match.group("primer_name")
    else:
        return None

def get_sequence_dna_number(sequence_filename):
    # Example sequence filename
    # &vDRMDNA0000_&g18S_&pPUB001_&aAF002790_&nPericompsus laetulus.fas
    dna_number_match = re.search("&vDRMDNA(?P<dna_number>\d+)", sequence_filename)

    if dna_number_match:
        return dna_number_match.group("dna_number")
    else:
        return None

def get_sequence_gene_name(sequence_filename):
    # Example sequence filename
    # &vDRMDNA0000_&g18S_&pPUB001_&aAF002790_&nPericompsus laetulus.fas
    gene_name_match = re.search("_&g(?P<gene_name>.+?)_", sequence_filename)

    if gene_name_match:
        return gene_name_match.group("gene_name")
    else:
        return None

def get_sequence_primers(sequence_filename, chromatogram_filenames, primers):
    sequence = { "forward_primers": [], "reverse_primers": [] }
    sequence_dna_number = get_sequence_dna_number(sequence_filename)
    sequence_gene_name = get_sequence_gene_name(sequence_filename)

    if chromatogram_filenames.has_key(sequence_dna_number):
        for chromatogram_filename in chromatogram_filenames[sequence_dna_number]:
            primer_name = get_chromatogram_primer(chromatogram_filename)

            if primer_name and primers.has_key(primer_name.upper()):
                primer = primers[primer_name.upper()]

                if primer["gene_name"] == sequence_gene_name:
                    if primer["type"] == "F":
                        sequence["forward_primers"].append(primer_name)
                    else:
                        sequence["reverse_primers"].append(primer_name)

    return sequence

def get_sequences(sequences_folder_path, chromatogram_filenames, primers):
    sequences = []

    for sequence_filename in os.listdir(sequences_folder_path):
        sequence = {}
        sequence.update(get_sequence_primers(sequence_filename, chromatogram_filenames, primers))
        sequence["dna_number"] = get_sequence_dna_number(sequence_filename)
        sequence["gene_name"] = get_sequence_gene_name(sequence_filename)
        sequences.append(sequence)

    return sequences

def get_genes(sequences):
    genes = {}

    for sequence in sequences:
        gene_name = sequence["gene_name"]

        if not genes.has_key(gene_name):
            genes[gene_name] = { "forward_primers": {}, "reverse_primers": {} }
        
        for primer_type in ["forward_primers", "reverse_primers"]:
            for primer in sequence[primer_type]:
                if not genes[gene_name][primer_type].has_key(primer):
                    genes[gene_name][primer_type][primer] = "|"

    return genes

def xstr(s):
    if s is None:
        return ''
    else:
        return str(s)

def save_sequences_file(sequences, filename):
    file_content = ""
    file_content += "dna_number\t"
    file_content += "gene_name\t"
    file_content += "forward_primers\t"
    file_content += "reverse_primers\n"

    for sequence in sequences:
        file_content += sequence["dna_number"] + "\t"
        file_content += xstr(sequence["gene_name"]) + "\t"
        file_content += ", ".join(sequence["forward_primers"]) + "\t"
        file_content += ", ".join(sequence["reverse_primers"]) + "\n"

    with open(filename, 'w') as f:
        f.write(file_content)

def main(sequences_folder_path, chromatograms_folder_path, primers_file_path):
    chromatogram_filenames = get_chromatogram_filenames(chromatograms_folder_path)
    primers = get_primers(primers_file_path)
    sequences = get_sequences(sequences_folder_path, chromatogram_filenames, primers)
    genes = get_genes(sequences)
    save_sequences_file(sequences, "sequences.csv")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sequences_folder")
    parser.add_argument("--chromatograms_folder")
    parser.add_argument("--primers_file")
    args = parser.parse_args()

    sequences_folder_path = os.path.join(os.getcwd(), "sequences")
    chromatograms_folder_path = os.path.join(os.getcwd(), "chromatograms")
    primers_file_path = os.path.join(os.getcwd(), "primers.csv")
    
    if args.sequences_folder:
        sequences_folder_path = args.sequences_folder
    
    if args.chromatograms_folder:
        chromatograms_folder_path = args.chromatograms_folder

    if args.primers_file:
        primers_file_path = args.primers_file

    main(sequences_folder_path, chromatograms_folder_path, primers_file_path)
