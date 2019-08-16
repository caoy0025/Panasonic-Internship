#!/bin/bash

index=0
inputfile="./liveextractplot.in"
outputfile=""
pythonfile="liveextractplot.py"

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
		if [[ $filenameline != "#"* ]]
		then
        	python $pythonfile $filenameline
		fi
    fi
done < $inputfile



