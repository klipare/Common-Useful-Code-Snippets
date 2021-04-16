#!/usr/bin/python

# This script is to merge all the files in a given directory and sort the contents in the final merged file. 
# This script requires Python version 3.x to be installed in the system

# The arguments for the scripts are:
#	-p or --path = takes the input of the full path of the directory in which files are to be merged (required)
#	-f or --filename = takes the input of new filename for the output file, that is, the final sorted merged file (required) 
#	-u or --unique = takes the input of y/n for deleting/keeping the duplicate contents while merging the file (optional)

# file_merge function, copies all the file objects into a single file in the given directory using shutil library module https://docs.python.org/2/library/shutil.html

# usage python <merge_sort.py> --path <directory_path> --filename <output_filename_to_store_result> --unique true
# usage python <merge_sort.py> -p <directory_path> -f <output_filename_to_store_result> -u 


import os
import sys
import shutil
import argparse

# To print the help message instead of invalid argument error while passing the arguments in command line
# overriding ArgumentParser class to display help instead of standard error

class LocalParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = LocalParser()

parser.add_argument("-p", "--path", required=True, help ="path of the folder or directory in which files are to be merged")
parser.add_argument("-f", "--filename", required=True, help = "filename for the output file")
parser.add_argument("-u", "--unique", help = "enter true to avoid duplicate entries in output file, default is False")

# To print the help message instead of traceback while no arguments have been passed with the arguments

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args() 

# assigning arguments to global variables

file_path = args.path
arg_filename = args.filename
is_unique = args.unique

cwd = os.getcwd() # get current working directory

# check for filename extension in argument, if not add the extension to output filename

if arg_filename.lower().endswith('.dat'):
	output_filename = arg_filename
else:
	file_extension = ".dat"
	output_filename = arg_filename + file_extension
	
# function to merge all the files from the given directory into one file using shutil module.

def file_merge():

# try/except method for error handling invalid directory
	try:
		files = os.listdir(file_path)
		with open(output_filename, "w") as file_out:
			for file in files:
				with open(os.path.join(file_path, file), "r") as file_in:
					shutil.copyfileobj(file_in, file_out)
		
	except OSError as msg:
		print("Given Directory path is not valid, Enter a valid directory path")
		exit()

		
# function to sort the content in alphabetical order from the merged file

def file_sort():
	with open(output_filename, "r") as file_in:
		lines = [line.split(' ') for line in file_in]
		with open(output_filename, "w") as tmp_file:
			for line in sorted(lines):
				tmp_file.write(' '.join(line))
	
		
# function to delete duplicate entries during file merge

def unique_content():
	lines_seen = set() # holds lines already seen
	outfile = "tempfile.dat" # creating a tempfile to store write the unique entries from merged&sorted file
	with open(outfile, "w") as fout:
		for line in open(output_filename, "r"):
			if line not in lines_seen: # not a duplicate
				fout.write(line)
				lines_seen.add(line)
	shutil.move(os.path.join(cwd, outfile), os.path.join(cwd, output_filename)) # replace the duplicate content file with unnique content file
	
	
def main():
	file_merge()
	file_sort()
	print("Total number of files merged", len([f for f in os.listdir(file_path)if os.path.isfile(os.path.join(file_path, f))]))
	print("The total size of the given directory is ", os.path.getsize(file_path), "bytes")
	print("The total size of merged file is", os.path.getsize(output_filename), "bytes")
	print("The output merged and sorted file path with duplicates is saved in", os.path.join(cwd,output_filename))
	print("The total size of sorted file with duplicate entries is", os.path.getsize(output_filename), "bytes")
	try:
		if is_unique.lower() == "true":
			unique_content()	
			print("The duplicate entries in sorted file are deleted")
			print("The total size of sorted file with duplicate entries deleted is", os.path.getsize(output_filename), "bytes")
	except:
		exit()
		
if __name__=='__main__':
	main()
