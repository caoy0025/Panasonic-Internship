import sys, math
import numpy as np
import matplotlib.pyplot as plt
import csv, itertools , xlwt ,operator
import pandas as pd
from collections import OrderedDict
import os
import matplotlib.lines as mlines
import os.path


SKIPFIRSTREADING = 1 # set to 1 to ignore first measurement (note: sometimes first readings are significantly worse)
typekeyword = ["type 13"]
keep_phrases = ["CTRL-EVENT-CONNECTED"]

#declaration
firstimestamp = float()
secondtimestamp = float()
latencytime = float()

# Get log file name and check if valid
if len(sys.argv) != 2:
	print( "Correct usage: python extractplot<ver>.py [dir]/[filename].csv")
	quit() # not valid so exit

if SKIPFIRSTREADING  == 1:
	print( "Note: Skip first reading: Enabled (to avoid abnormal values)")

inputlogfile = sys.argv[1]

inputlogfiledir = str(inputlogfile.rsplit('/',1)[0]) + "/"

inputlogfilename = os.path.basename(inputlogfile)

inputlocation = inputlogfiledir + "Results/latencyfile.log"

file_exists = os.path.isfile(inputlocation) #Checks if file is present in folder


with open(inputlocation, "a") as supfile:
	writer4 = csv.DictWriter(supfile, fieldnames = ["Distance", "mcs", "latency", "sup_file_name"], delimiter = ',' )
	
	if not file_exists:
		writer4.writeheader() # file doesn't exist yet, write a header

supfile.close()


with open(inputlogfile, "rt") as inputlog: #Input main file name
	inputlogcontent = inputlog.readlines()[1:]
	for line in inputlogcontent:

		distance = line.split(",")[2] #find x axis
		mcs = line.split(",")[5] #find mcs
		supFilePathName = inputlogfiledir + str(line.split(",")[8]) #find sup files
		supFilename = line.split(",")[8]


		with open(supFilePathName, "rt") as SupFile:
			SupFilelines = SupFile.readlines()

			for lines in SupFilelines:
				if "type 13" in lines:
					firstimestamp = lines.split(" ")[0]
					break

			for lines in SupFilelines:	#not very efficient
				if "CTRL-EVENT-CONNECTED" in lines:
					secondtimestamp = lines.split(" ")[0]
					break

			latencytime = float(secondtimestamp) - float(firstimestamp)

			inputline = distance + "," + mcs + "," + str(latencytime) + "," + supFilename + "\n"

			with open(inputlocation, "a") as supfile:
				supfile.write(inputline)
			supfile.close()	


	

print( "\nSummary:")
print( "Input:")
print( inputlogfile)
print( "Output:")
print( inputlocation)




			
