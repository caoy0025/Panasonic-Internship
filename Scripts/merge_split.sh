#!/bin/bash

index=0
inputfile="./merge_split.in"
outputfile=""

if [ "$1" ] 
	then
	inputfile="./"$1
fi

# Get the output file name
while read filenameline ; do
    pathname=$(basename -- "$filenameline")
    filename="${pathname%.*}"
    # Check if filename contains "log_"
    if [[ $filename = *"log_"* ]]
    then
        if [ "$index" = "0" ]
        then
            extension="${pathname##*.}"
            # first file keeps directory info
            outputfile="${filenameline%.*}"
            #echo $outputfile
        else
            # subsequent files extract only timing
            thisfilestring=$(echo $filename | cut -d "_" -f3)
            outputfile=$outputfile"_"$thisfilestring
            #echo $outputfile
        fi
    fi
    index=$((index+1))
done < $inputfile

outputfile=$outputfile"."$extension
echo "Merged log file: "$outputfile 

index=0

# Write the output file contents
while read filenameline ; do
    if [ "$index" = "0" ]
    then
        # first file keeps header and deletes comments
        # remove line with comments
        sed '/Comments/d' $filenameline > $outputfile
    else
        # subsequent files delete header and comments
        sed '/yyyymmdd_hhmmss/d;/Comments/d' $filenameline >> $outputfile
    fi
    index=$((index+1))
done < $inputfile


python mcssplit.py $outputfile





