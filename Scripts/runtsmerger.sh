#!/bin/bash

index=0
inputfile="./runtsmerger.in"
outputfile=""
pythonfile="tsmerger10.py"

if [ "$1" ] 
	then
	inputfile="./"$1
fi

# Get input files info
while read filenameline ; do
    pathname=$(basename -- "$filenameline")
    folderpath=$(dirname "${filenameline}")
    filename="${pathname%.*}"

    # Check if filename contains "log_"
    if [[ $filename = *"log_"* ]]
    then
        # Create output folder if not yet there
        mkdir -p $folderpath/Results
        python $pythonfile $filenameline
    fi
done < $inputfile



