##########################
##### MXD File Merger ####
##########################
## Author: Josh Wilkins ##
##########################

## Run in same directory as data to be merged
## Merges all mxd files in folder to csv files by MacD P6 part number
## Moves original mxd files int "OldFiles" directory

# This is a line by line method of merging the files
# Important to note that this method is slower, but won't run into memory issues!

import glob
import os

mxd_files = sorted(glob.glob(".\\OldFiles\\*.mxd") ) # Get and sort the moved mxd files in folder

device = mxd_files[0][:mxd_files[0].find("[")]  # Get device Serial Number of first file
new_device = device
f_out = open(csv_dir + new_device + ".csv", 'wb')
writer = csv.writer(f_out, delimiter=',', quoting=csv.QUOTE_MINIMAL)
writer.writerow(["MJD", "F1s"])
for mxd_file in mxd_files:
    new_device = mxd_file[0 : mxd_files[0].find("[")]  # Get device Serial Number of first file
  
    if new_device != device:
        f_out.close()
        f_out = open(csv_dir + new_device + ".csv", 'wb')
        writer = csv.writer(f_out, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["MJD", "F1s"])
        device = new_device
  
    with open(mxd_file ,"rb") as f_in:
        # Read header to get indices of columns
        reader = csv.reader(f_in, quoting=csv.QUOTE_NONE, dialect='excel')
        header = next(reader)

        mjd_index = header.index("MJD")
        freq_index = header.index("F1s")
      
        for row in reader:
            writer.writerow([row[mjd_index]] + [row[freq_index]])

f_out.close()