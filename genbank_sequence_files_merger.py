# Merges multiple GenBank Sequence files into one csv file
import os
import sys

def get_sequence(filename):
	with open(filename, 'r') as f:
		return f.read().split('\n')[1]

	return ""

def save_file(filename, file_content):
	with open(filename, 'w') as f:
		f.write(file_content)

def main(argv):
	if len(argv) < 2:
		print("Filename for csv file containing GenBank Sequences must be provided!")
		return

	new_filename = argv[1]
	file_headers = ["filename", "file_content"]
	file_content = ""

	for header in file_headers:
		file_content += header + "\t"

	file_content += "\n"

	for filename in os.listdir(os.getcwd()):
		if filename[0] != "&":
			continue
		
		print(filename)

		file_content += filename + "\t"
		file_content += get_sequence(filename) + "\t"
		file_content += "\n"

	save_file(new_filename, file_content)

if __name__ == "__main__":
	main(sys.argv)