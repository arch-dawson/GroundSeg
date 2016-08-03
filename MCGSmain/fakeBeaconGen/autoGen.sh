#!/bin/bash
# This script is used to generate fake beacons
# Has 'allstarcosgc' as header and footer
# 120 bytes of artificial hex data
# Assumes autoGen.sh is in an adjacent folder to testFiles 

#======ENTER FOLDER FOR GENERATED FILES======
path=$1 # Absolute path as first command line argument

headerStr=$(od -A n -t x1 header) # Gets the header from the 'header' file, converts to hex

headerStr=${headerStr//[[:space:]]/} # Removes spaces

cd $path #Folder to create files in 

str="testFile$(date +%s)"  # Creating file name with date stamp

touch $str # Creating the actual file 

#headerStr=${headerStr:0:30} # Remove newline character

data=$(openssl rand -hex 120) # Create 120 random hex bytes

outStr="$headerStr$data$headerStr" # Combine two headers and data into one string

#echo $outStr >> $path/$str # Append outStr to file
echo $outStr >> $str # Write outStr to file




