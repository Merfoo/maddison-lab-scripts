import os
import csv
import argparse

def xstr(s):
    if s is None:
        return ""
    else:
        return str(s)

def main(folder_path, primers_filename, output_primers_filename):
    primers_file_path = os.path.join(folder_path, primers_filename)
    output_primers_file_path = os.path.join(folder_path, output_primers_filename)
    file_content = ""
    file_content += "name\t"
    file_content += "gene_name\t"
    file_content += "type\t"
    file_content += "sequence\n"

    with open(primers_file_path, "rb") as csv_file:
        primers_reader = csv.reader(csv_file, delimiter="\t")

        for index, row in enumerate(primers_reader):
            if index == 0:
                continue

            file_content += xstr(row[0]).upper() + "\t"
            file_content += row[1] + "\t"
            file_content += row[2] + "\t"
            file_content += row[3] + "\n"

    with open(output_primers_filename, "w") as f:
        f.write(file_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_path")
    parser.add_argument("--primers_filename")
    parser.add_argument("--output_primers_filename")
    args = parser.parse_args()

    folder_path = os.getcwd()
    primers_filename = "primers.csv"
    output_primers_filename = ""

    if args.folder_path:
        folder_path = args.folder_path

    if args.primers_filename:
        primers_filename = args.primers_filename

    if args.output_primers_filename:
        output_primers_filename = args.output_primers_filename
    else:
        output_primers_filename = "uppercased-" + primers_filename
        
    main(folder_path, primers_filename, output_primers_filename)
