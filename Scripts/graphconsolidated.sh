#!/bin/bash

index=0
inputfile="./graphconsolidated.in"
outputfile=""
pythonfile="graphconsolidated.py"

if [ "$1" ] 
	then
	inputfile="./"$1
fi

echo -n "" > $inputfile.tmp

# Get input files info //RUN ONCE//
while read filenameline ; do

	# auto comment out after line processed
	echo $filenameline >> $inputfile.tmp

    pathname=$(basename -- "$filenameline")
    folderpath=$(dirname "${filenameline}")
    filename="${pathname%.*}"

    if [[ $filenameline != "#"* ]] 
    then
        python $pythonfile $filenameline
    fi
done < $inputfile

mv $inputfile.tmp $inputfile

