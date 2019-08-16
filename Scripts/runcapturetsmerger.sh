#!/bin/bash

index=0
inputfile="./runcapturetsmerger.in"
outputfile=""
pythonfile="capturetsmerger.py"

if [ "$1" ] 
	then
	inputfile="./"$1
fi

# Get input files info
while read foldernameline ; do
    pathname=$(basename -- "$foldernameline")
    folderpath=$(dirname "${foldernameline}")

    # Check if filename contains "/"
    if [[ $foldernameline = *"/"* ]]
    then
        # Create output folder if not yet there
        mkdir -p $folderpath/Results
        mkdir -p $folderpath/Results/Tsmergedata
        mkdir -p $folderpath/Results/Tsmergedata/Datatype
        python $pythonfile $folderpath/$pathname
    fi
done < $inputfile



