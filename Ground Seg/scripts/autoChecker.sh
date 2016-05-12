#!/bin/bash

#======FOLDER TO BE CHECKED=======
path="../testFiles/"

#======FOLDER WITH MOST RECENT FILE======
mrPath="../scripts/"

cd $path 

lastFile=$(ls | sort -n | tail -n 1)

newData=$(cat $lastFile)

fileTimeStamp="${lastFile//[!0-9]/}" 

cd $mrPath

pastTimeStamp=$(cat mostRecentStamp)

if [ "$pastTimeStamp" != "$fileTimeStamp" ]; then
    echo $fileTimeStamp > mostRecentStamp
    echo $newData > mostRecent
    #python generalReader.py
fi
