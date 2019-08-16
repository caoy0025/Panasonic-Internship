import csv, itertools , xlwt , sys , os
import time
import pandas as pd
from io import StringIO
from shutil import copyfile


## main 
Header = "yyyymmdd_hhmmss,target,distance,placement,offset,fin_mcs,notes,prsconfig_file,sup_file,init_config_file,ping_file,udp_file,tcp_file,apd_file,statssup_file,statsapd_file\n"

# Get log file name and check if valid
if len(sys.argv) != 2:
	print( "Correct usage: python mcssplit<ver>.py [dir]/[filename].csv")
	quit() # not valid so exit

inputlogfile = sys.argv[1]
# inputlogfiledir = os.path.dirname(os.path.realpath(inputlogfile)) + "/"
inputlogfiledir = str(inputlogfile.rsplit('/',1)[0]) + "/"
inputlogfilename = os.path.basename(inputlogfile)
outputlogfilebase = inputlogfiledir + inputlogfilename[:-4]+"_mcs"+inputlogfilename[-4:]

try:
	with open(inputlogfile , "rt") as tempfile:
		donothing=1
except IOError:
	print( "ERROR (IOERROR: " + inputlogfile +" not found)")
	quit()

listfinmcs = []

with open(inputlogfile, "rt") as inputlog: #Input main file name
	skipheader=1
	for lines in inputlog:
		# skip header line
		if skipheader == 1:
			skipheader=0
		else:			
			#get fin_mcs (available values: -,1,4,9,12)
			fin_mcs_val = str(lines.split(",")[5]) #finds fin_mcs
			outputlogfile = outputlogfilebase[:-4]+fin_mcs_val+outputlogfilebase[-4:]
			if fin_mcs_val in listfinmcs:
				with open(outputlogfile, 'a+') as outputlog:				
					outputlog.write(lines)
			else:
				with open(outputlogfile, 'w+') as outputlog:				
					listfinmcs.append(fin_mcs_val)
					outputlog.write(Header)
					outputlog.write(lines)
			outputlog.close()

inputlog.close()

print( "\nSummary:")
print( "Input:")
print( inputlogfile)
print( "Output:")
for item in listfinmcs:
	outputlogfile = outputlogfilebase[:-4]+item+outputlogfilebase[-4:]
	print( outputlogfile)