#!/bin/bash
# This script is used to generate fake beacons
# Has 'allstarcosgc' as header and footer
# 120 bytes of artificial hex data

cd /home/dawson/testFiles/ #Folder to create files in 

str="testFile$(date +%s)"  # Creating file name with date stamp

touch str # Creating the actual file

headerStr=$(od -A n -t x1 header) # Gets the header from the 'header' file, converts to hex

headerStr=${headerStr//[[:space:]]/} # Removes spaces 

headerStr=${headerStr:0:30} # Remove newline character

data=$(openssl rand -hex 120) # Create 120 random hex bytes

outStr="$headerStr$data$headerStr" # Combine two headers and data into one  string

echo $outStr >> /home/dawson/testFiles/$str # Append outStr to file





