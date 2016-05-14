#!/bin/bash

#======FOLDER TO BE CHECKED=======
path="../testFiles/"

#======FOLDER WITH MOST RECENT FILE======
mrPath="../scripts/"

pastTimeStamp=$(cat mostRecentStamp)

cd $path 

todoCount=0

for temp in $(ls | sort -n -r); do # Sorts with newest first
    fileTimeStamp="${temp//[!0-9]/}"
    if [ "$pastTimeStamp" == "$fileTimeStamp" ]; then
	break
    fi
    todoCount=$((todoCount+1))
done

for file in $(ls | sort -n -r | head -n $todoCount); do
    newData=$(cat $file)
    echo $file > ../scripts/mostRecent
    #python ../scripts/generalReader.py
done

mostRecentFile=$(ls | sort -n -r | head -n 1)

echo ${mostRecentFile//[!0-9]/} > ../scripts/mostRecentStamp
