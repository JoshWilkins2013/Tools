##########################
##### MXD File Merger ####
##########################
## Author: Josh Wilkins ##
##########################

## Run in same directory as data to be merged
## Merges all mxd files in folder to csv files by MacD P6 part number
## Moves original mxd files int "OldFiles" directory

import glob
import os

files = sorted(glob.glob("*.mxd") ) # Get and sort mxd files in folder

# Create new directory for the files being merged
if not os.path.exists(".\\OldFiles\\"):
	os.makedirs(".\\OldFiles\\")

for filename in files:
	new_path = ".\\OldFiles\\" + filename
	os.rename(filename, new_path)  # Move old files into new directory

files = sorted(glob.glob(".\\OldFiles\\*.mxd") ) # Get and sort the moved mxd files in folder
device = files[0][11:22]  # Serial Number of device
new_file = files[0][11:]
fout = open(new_file, 'wb')
header_saved = False  # Only keep header from one file
for filename in files:
	new_device = filename[11:22]
	if new_device != device:
		device = new_device
		new_file = filename[11:]
		fout = open(new_file, 'a')
		header_saved = False  # Only keep header from one file
	with open(filename) as fin:
		header = next(fin)
		if header_saved:  # Skip header and first few lines of data
			for _ in range(3):
				next(fin)
		else:  # Keeping header and first few lines from first file
			fout.write(header)
			header_saved = True
		for line in fin:
			fout.write(line)  # Write contents of each file into merged file
	fin.close()