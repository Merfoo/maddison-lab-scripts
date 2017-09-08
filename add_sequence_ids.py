import os
import sys

def main(dir_path):
    for index, filename in enumerate(os.listdir(dir_path)):
        file_path = os.path.join(dir_path, filename)
        new_filename = "&iSEQID" + str(index).rjust(8, "0") + "_" + filename
        new_file_path = os.path.join(dir_path, new_filename)
        os.rename(file_path, new_file_path)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Path to sequences must be provided!")