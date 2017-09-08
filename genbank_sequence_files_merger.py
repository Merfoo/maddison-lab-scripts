# Merges multiple GenBank Sequence files into one csv file
import os
import argparse

def get_sequence(filename):
    with open(filename, 'r') as f:
        return f.read().split('\n')[1]

    return ""

def save_file(filename, file_content):
    with open(filename, 'w') as f:
        f.write(file_content)

def main(filename, sequences_folder_path):
    file_headers = ["filename", "file_content"]
    file_content = ""

    for header in file_headers:
        file_content += header + "\t"

    file_content += "\n"

    for sequence_filename in os.listdir(sequences_folder_path):
        if sequence_filename[0] != "&":
            continue
        
        sequence_file_path = os.path.join(sequences_folder_path, sequence_filename)
        print(sequence_filename)

        file_content += sequence_filename + "\t"
        file_content += get_sequence(sequence_file_path) + "\t"
        file_content += "\n"

    save_file(filename, file_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename")
    parser.add_argument("--sequences_folder_path")
    args = parser.parse_args()

    filename = "sequences.csv"
    sequences_folder_path = os.getcwd()

    if args.filename:
        filename = args.filename

    if args.sequences_folder_path:
        sequences_folder_path = args.sequences_folder_path

    main(filename, sequences_folder_path)
    