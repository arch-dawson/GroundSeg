#!/bin/bash
# First command line argument is the absolute path from code to folder with files to be parsed
# Second command line argument is the most Recent file so the code knows where to stop

mostRecentFile=$2

mostRecentContents=$(cat $mostRecentFile)

pastTimeStamp="${mostRecentContents//[!0-9]/}"

todoCount=0

for temp in $(ls $1 | sort -n -r); do # Sorts with newest first
    fileTimeStamp="${temp//[!0-9]/}" # Strip time stamp
    if [ "$pastTimeStamp" == "$fileTimeStamp" ]; then  # If we've gone through all the new files
	break
    fi
    todoCount=$((todoCount+1))
done

newMostRecent=$(ls $1 | sort -n -r | head -n 1) # Recording where we've checked up to 

if (($todoCount > 0)); then
    echo $(ls $1 | sort -n -r | head -n $todoCount) # python script running this will read output here
fi

echo $newMostRecent > $mostRecentFile
