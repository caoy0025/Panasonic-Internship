import csv, itertools , xlwt , sys , os
import time
import pandas as pd
from io import StringIO
from shutil import copyfile

ENTERKEYCHARSPACE = 0 # \r\n #.split removes the \r\n
TIMESTAMPLENGTH = 17 # hardcoded!
OUTPUT_FOLDER = "Results/"
OUTPUT_FOLDER2 = "Test/"

def twos_comp(val, bits): #"""compute the 2's complement of int value val"""
	if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
		val = val - (1 << bits)        # compute negative value
	return val                         # return positive value as is


def hex_to_dex(strng_of_hex):
	return int(strng_of_hex, 16)

def remove_quotes(s):
	return ''.join(c for c in s if c not in ('"', "'"))


def timestampMerge( srcfilename1, srcfilename2, dstfilename, mergecount1, mergecount2 ):

	#print( "merge: " + srcfilename1 + " and " + srcfilename2

	listOfSecondFileLines = []

	# check if either source files are '-'
	if len(srcfilename1) == len(inputlogfiledir)+1: # I.e. is '-'
		srcfilename1 = "blankfile1.tmp"
		with open(srcfilename,"w") as tempfile1:
			tempfile1.write(" ")
		tempfile1.close()
	# check if either source files are '-'
	if len(srcfilename2) == len(inputlogfiledir)+1: # I.e. is '-'
		srcfilename2 = "blankfile2.tmp"
		with open(srcfilename2,"w") as tempfile2:
			tempfile2.write(" ")
		tempfile2.close()
	
	if mergecount1 > 0:
		firstfilemergespace = 1
	else:
		firstfilemergespace = 0
	if mergecount2 > 0:
		secondfilemergespace = 1
	else:
		secondfilemergespace = 0

#open files and gets timestamp of each file puts all timestamps into a list
	try:
		with open(srcfilename1 , "rt") as firstFile:
			first_file = firstFile.read().splitlines()[1:] #reads second file (first file)
			#first_file = (first_file.rstrip() for lines in firstFile)
	except IOError:
		print( "WARNING (IOERROR: " + srcfilename1 +" not found, mergecount=" + str(mergecount1+mergecount2) + ")")
		os.remove(dstfilename)
		return -1
			
	try:	
		with open (srcfilename2, "rt") as secondFile:
			second_file = secondFile.read().splitlines()[1:] #reads first file (second file)
			# second_file = second_file.rstrip()
			for line in second_file:
				timeStampSecondfile = line.split(" ")[0]
				listOfSecondFileLines.append(line) # Converts all contents of second file into new list
	except IOError:
		print( "WARNING (IOERROR: " + srcfilename2 +" not found, mergecount=" + str(mergecount1+mergecount2) + ")")
		os.remove(dstfilename)
		return -1

	secondFilelastIndex=-1

	with open(dstfilename, "w") as csvout: #output file name
		# Create header (note: important since merge input is assumed to have header line)
		# for now, only timestamp is named header
		csvline = "timestamp,Sup,Udp,Tcp,Stat" 
		for loopindex in range(mergecount2+1):
			csvline = csvline + ","
		csvout.write(csvline + "\n")

		for line in first_file:
			timeStampFirstfile = line.split(" ")[0]
			lineLength=len(line)
			lineLength = lineLength
			currentSecondFileIndex=-1

			# check if line has timestamp
			if len(timeStampFirstfile) <= 2: # '2' may avoid blank and special characters also
				# no timestamp
				continue # go to next line
			
#Enter lines for second file
			for secondfileLines in listOfSecondFileLines:
				currentSecondFileIndex=currentSecondFileIndex+1
				timeStampSecondfile = secondfileLines.split(" ")[0]
				#print( timeStampSecondfile
				# check if secondrow has timestamp
				if len(timeStampSecondfile) <= 2 or len(timeStampSecondfile) > 17: # '2' may avoid blank and special characters also  
					# no timestamp
					secondFilelastIndex=currentSecondFileIndex	# update secondFilelastIndex in case this is the last line
					continue # check next line
#Clears timestamp second file data if print(ed (prevets double print(ing)
				if currentSecondFileIndex > secondFilelastIndex:
					if timeStampSecondfile < timeStampFirstfile: 
						csvline = timeStampSecondfile + " "
						for loopindex in range(mergecount1+1):
							csvline = csvline + ",-"
						csvline = csvline + ","+ secondfileLines[TIMESTAMPLENGTH+1+secondfilemergespace:]				
						csvout.write(csvline + "\n")
						secondFilelastIndex=currentSecondFileIndex

					elif timeStampSecondfile == timeStampFirstfile:
						csvline = timeStampFirstfile + " " + "," +line[TIMESTAMPLENGTH+1+firstfilemergespace:lineLength-ENTERKEYCHARSPACE] + "," + secondfileLines[TIMESTAMPLENGTH+1+secondfilemergespace:]
						csvout.write(csvline + "\n")
						secondFilelastIndex=currentSecondFileIndex
						break

					else: #timeStampSecondfile>timeStampFirstfile	
						csvline = timeStampFirstfile + " " + "," +line[TIMESTAMPLENGTH+1+firstfilemergespace:lineLength-ENTERKEYCHARSPACE]
						for loopindex in range(mergecount2+1):
							csvline = csvline + ",-"
						csvout.write(csvline + "\n")
						break

# print( line if no more secondfileLines to compare with (i.e. all secondfileLines lines have been print(ed)
			if secondFilelastIndex == (len(listOfSecondFileLines)-1):
				csvline = timeStampFirstfile + " " + "," +line[TIMESTAMPLENGTH+1+firstfilemergespace:lineLength-ENTERKEYCHARSPACE]
				for loopindex in range(mergecount2+1):
					csvline = csvline + ",-"
				csvout.write(csvline + "\n")


#print(s every second file row that has not been print(ed
		currentSecondFileIndex=-1
		for secondfileLines in listOfSecondFileLines:
			# check if timestamp exists
			timeStampSecondfile = secondfileLines.split(" ")[0]

			if len(timeStampSecondfile) <= 2: # '2' may avoid blank and special characters also
# no timestamp 
				secondFilelastIndex=currentSecondFileIndex	# update secondFilelastIndex 
				continue # check next line
			currentSecondFileIndex=currentSecondFileIndex+1


			if secondFilelastIndex < currentSecondFileIndex:
				csvline = timeStampSecondfile + " "
				for loopindex in range(mergecount1+1):
					csvline = csvline + ",-"
				csvline = csvline + "," + secondfileLines[TIMESTAMPLENGTH+1+secondfilemergespace:]
				csvout.write(csvline + "\n")
				secondFilelastIndex=secondFilelastIndex+1
	firstFile.close()
	secondFile.close()
	csvout.close()
	return 0


## main 
Header = "yyyymmdd_hhmmss,target,distance,placement,offset,fin_mcs,notes,prsconfig_file,sup_file,init_config_file,ping_file,udp_file,tcp_file,apd_file,statssup_file,statsapd_file,output_timestamp_merged_files\n"

#Get log file name and check if valid
if len(sys.argv) != 2:
	print( "Correct usage: python tsmerger<ver>.py [dir]/[filename].csv")
	quit() # not valid so exit

inputlogfile = sys.argv[1]
# inputlogfiledir = os.path.dirname(os.path.realpath(inputlogfile)) + "/"
inputlogfiledir = str(inputlogfile.rsplit('/',1)[0]) + "/"
inputlogfilename = os.path.basename(inputlogfile)
outputlogfile = inputlogfiledir + OUTPUT_FOLDER + inputlogfilename[:-4]+"_tsmerge"+inputlogfilename[-4:]
mergedfilenamelist = []

try:
	with open(inputlogfile , "rt") as tempfile:
		donothing=1
except IOError:
	print( "ERROR (IOERROR: " + inputlogfile +" not found)")
	quit()

with open(inputlogfile, "rt") as inputlog: #Input main file name
#Creates temp updated log file
	with open(outputlogfile, 'w') as outputlog:
		outputlog.write(Header)
		next(inputlog)
		#inputlog = inputlog.readlines()[1:]
		for lines in inputlog:
			datetime = str(lines.split(",")[0]) #finds datetime from log file
			distance = str(lines.split(",")[2])
			fileToexport = inputlogfiledir + str(lines.split(",")[11]) #finds first file eg:udp.log
			#print( fileToexport
			fileToexport2 = inputlogfiledir + str(lines.split(",")[8]) #find second file eg:Sup.log
			#print( fileToexport2
			fileToexport3 = inputlogfiledir + str(lines.split(",")[12]) #find third file eg:tcp.log
			#print( fileToexport3
			fileToexport4 = inputlogfiledir + str(lines.split(",")[14]) #find third file eg:tcp.log
			#print( fileToexport3

			if len(fileToexport2) == len(inputlogfiledir)+1: # I.e. is '-'
				print( "NOTE: " + datetime + " " +distance + "m Sup file not included")
				outputlog.write(lines.rstrip()+"\n")
				continue
			else:
				try:
					with open(fileToexport2,"r") as tempfile:		
						donothing=1			
					tempfile.close()
				except:
					print( "WARNING (IOERROR: " + fileToexport2 +" not found - SKIP ROW)")
					continue

				if len(fileToexport) != len(inputlogfiledir)+1: # I.e. not '-'
					try:
						with open(fileToexport,"r") as tempfile:		
							donothing=1			
						tempfile.close()
					except:
						print( "WARNING (IOERROR: " + fileToexport +" not found - IGNORE)")
						fileToexport = inputlogfiledir + "-"

				if len(fileToexport3) != len(inputlogfiledir)+1: # I.e. not '-'
					try:
						with open(fileToexport3,"r") as tempfile:		
							donothing=1			
						tempfile.close()
					except:
						print( "WARNING (IOERROR: " + fileToexport3 +" not found - IGNORE)")
						fileToexport3 = inputlogfiledir + "-"

				if len(fileToexport4) != len(inputlogfiledir)+1: # I.e. not '-'
					try:
						with open(fileToexport4,"r") as tempfile:		
							donothing=1			
						tempfile.close()
					except:
						print( "WARNING (IOERROR: " + fileToexport4 +" not found - IGNORE)")
						fileToexport4 = inputlogfiledir + "-"



				filetomerge1 = inputlogfiledir + "-"
				filetomerge2 = inputlogfiledir + "-"
				filetomerge3 = inputlogfiledir + "-"

				if len(fileToexport) != len(inputlogfiledir)+1: # I.e. not '-'
					readerudp = list(csv.reader(open(fileToexport, "rU"), delimiter=','))
					with open ("outputudp.csv", 'w') as outputFileudp:
						writerudp = csv.writer(outputFileudp, delimiter=';', quotechar= "'")
						writerudp.writerows(readerudp)
					outputFileudp.close()
				fileToexport = "outputudp.csv"

				# Changes sup files double quotes to single quotes, sup data from "," to ";" 
				if len(fileToexport2) != len(inputlogfiledir)+1: # I.e. not '-'
					# Replacing double quotes with single quotes
					with open(fileToexport2,"r") as infile:
						with open("fixed.csv","w") as outfile:
							reader1 = csv.reader(infile)
							writer1 = csv.writer(outfile)
							for line in reader1:
								writer1.writerow([remove_quotes(elem) for elem in line])
						outfile.close()
					infile.close()

					#Changing from comma to semicolon Sup file
					reader = list(csv.reader(open("fixed.csv", "rU"), delimiter=','))
					with open ("output2.csv", 'w') as outputFile:
						writer = csv.writer(outputFile, delimiter=';', quotechar= "'")
						writer.writerows(reader)
					outputFile.close()

					
					with open('output2.csv', 'r') as inp, open('output.csv', 'w') as out:					
						writer = csv.writer(out)
						skipflag = 0 				
						for row in csv.reader(inp):		
							#print( str(row).split(" ")[1]
							if str(row).split(" ")[1] != "BF-EVENT:" and str(row).split(" ")[1] != "LINK-EVENT:" and str(row).split(" ")[1] != "PRS-EVENT-CUSTOM" and '/' not in str(row):
								if skipflag == 0:					  
									writer.writerow(row)
								skipflag = 0
							else:
								skipflag = 1
					filetomerge1 = "output.csv"


				if len(fileToexport3) != len(inputlogfiledir)+1: # I.e. not '-'
					#changing comma in Tcp file
					reader2 = list(csv.reader(open(fileToexport3, "rU"), delimiter=','))
					with open ("output3.csv", 'w') as outputFile2:
						writer2 = csv.writer(outputFile2, delimiter=';', quotechar= "'")
						writer2.writerows(reader2)
					outputFile2.close()
					filetomerge2 = "output3.csv"


				# Changes stat files from "," to ";" and changes data from hex to decimal and into 2's compliment
				if len(fileToexport4) != len(inputlogfiledir)+1: # I.e. not '-'
					#changing comma in Stat file
					reader3 = list(csv.reader(open(fileToexport4, "rU"), delimiter=','))
					with open ("output4.csv", 'w') as outputFile3:
						writer3 = csv.writer(outputFile3, delimiter=';', quotechar= "'")
						writer3.writerows(reader3)
					outputFile3.close()


					with open('output4.csv', 'r') as inpmerger, open('outputtomerge.csv', 'w') as outmerger:					
						writer1= csv.writer(outmerger)	
						for row1 in csv.reader(inpmerger):
						
							if len(row1[0]) >= 18 and  str(row1).split(" ")[1] == "STATS-EVENT-DATA:": 
								
								timetampdata = str(row1).split(" ")[0]
								timetampdata = timetampdata.replace("['","")
								

								data = str(row1).split(" ")[2]
								data = data.replace("']","")
								
								if len(data) == 24: # Checks ideal length of stat data while data is in hexadecimal: len(data) when data fails is less than 24

									BestBeamSNRData = data.split(';')[0]

								#### These commented lines are used to convert data to decimal and creates list of data ####

									#BestBeamSNRData = hex_to_dex(BestBeamSNRData)
									#BestBeamSNRData = twos_comp(BestBeamSNRData, 8)
									
									# BestBeamSNRDataList = BestBeamSNRDataList + [str(BestBeamSNRData)]
									# TotalBestBeamSNR = TotalBestBeamSNR + float(BestBeamSNRData)

									LastRemoteRssiData = data.split(';')[1]
									#print( LastRemoteRssiData
									#LastRemoteRssiData = hex_to_dex(LastRemoteRssiData)
									#LastRemoteRssiData = twos_comp(LastRemoteRssiData , 8)
									
									# LastRemoteRssiDataList = LastRemoteRssiDataList + [str(LastRemoteRssiData)]
									# TotalLastRemoteRssi = TotalLastRemoteRssi + float(LastRemoteRssiData)

									LastBeaconRssiData = data.split(';')[2]
									#LastBeaconRssiData = hex_to_dex(LastBeaconRssiData) 
									#LastBeaconRssiData = twos_comp(LastBeaconRssiData, 8)
									
									# LastBeaconRssiDataList = LastBeaconRssiDataList + [str(LastBeaconRssiData)]
									# TotalLastBeaconRssi = TotalLastBeaconRssi + float(LastBeaconRssiData)

									LastDataRssiData = data.split(';')[3]
									#LastDataRssiData = hex_to_dex(LastDataRssiData)
									#LastDataRssiData = twos_comp(LastDataRssiData, 8)
						
									# LastDataRssiDataList = LastDataRssiDataList + [str(LastDataRssiData)]
									# TotalLastDataRssi = TotalLastDataRssi + float(LastDataRssiData)

									CurrentMcsData = data.split(';')[4]
									#CurrentMcsData = hex_to_dex(CurrentMcsData)
							
									# CurrentMcsDataList = CurrentMcsDataList + [str(CurrentMcsData)]


									RFTempData = data.split(';')[5]
									#RFTempData = hex_to_dex(RFTempData)
									#RFTempData = twos_comp(RFTempData, 16)
								
									# RFTempDataList = RFTempDataList + [str(RFTempData)]
									# TotalRFTemp = TotalRFTemp + float(RFTempData)
								

									BBTempData = data.split(';')[6]
									#BBTempData =  hex_to_dex(BBTempData)
									#BBTempData = twos_comp(BBTempData, 16)
					
									# BBTempDataList = BBTempDataList + [str(BBTempData)]
									# TotalBBTemp = TotalBBTemp + float(BBTempData)
								else:

									BestBeamSNRData = "FAIL"

									LastRemoteRssiData = "FAIL"

									LastBeaconRssiData = "FAIL"

									LastDataRssiData = "FAIL"

									CurrentMcsData = "FAIL"

									RFTempData = "FAIL"
								
									BBTempData = "FAIL"

								convertedrow = str(timetampdata) + " STATS-EVENT-DATA: "+ str(BestBeamSNRData) + ";" + str(LastRemoteRssiData)  + ";" + str(LastBeaconRssiData) + ";" + str(LastDataRssiData) + ";" + str(CurrentMcsData) + ";" + str(RFTempData) + ";" + str(BBTempData)
								convertedrow = [convertedrow] #converting to list 
				
						
								writer1.writerow(convertedrow) #writerow (data) must be list
					filetomerge3 = "outputtomerge.csv"

				tempfilename = "temp.csv"				
				mergedfilename = "temp2.csv"
				#mergedfilename = inputlogfiledir + OUTPUT_FOLDER + "output_tsmerge_" + inputlogfilename[:-4]+"_distance" + distance+inputlogfilename[-4:]
				mergedfilename2 = inputlogfiledir + OUTPUT_FOLDER + "output_tsmerge_" + inputlogfilename[:-4]+"_distance" + distance+inputlogfilename[-4:]
				mergedfilenamelist=mergedfilenamelist+[mergedfilename2]


				with open (tempfilename, 'w') as tempfile:
					# creates file and does nothing else
					donothing=1
				tempfile.close()

				with open (mergedfilename, 'w') as mergedfile:
					# creates file and does nothing else
					donothing=1
				mergedfile.close()

				with open (mergedfilename2, 'w') as mergedfile2:
					# creates file and does nothing else
					donothing=1
				mergedfile2.close()

				mergecounter1=0
				mergecounter2=0
				success1 = timestampMerge(filetomerge1,fileToexport, tempfilename,mergecounter1,mergecounter2) #Combining Sup and Udp into Temp file
				mergecounter1 = mergecounter1 + 1
				success2 = timestampMerge(tempfilename,filetomerge2, mergedfilename,mergecounter1,mergecounter2) # Combining Temp file with Tcp
				mergecounter1 = mergecounter1 + 1
				success3 = timestampMerge(mergedfilename,filetomerge3, mergedfilename2,mergecounter1,mergecounter2) # Combining "New" Temp file with Stat


				try:
					os.remove("output.csv")
				except:
					donothing=1
				try:
					os.remove("outputudp.csv")
				except:
					donothing=1	
				try:
					os.remove("fixed.csv")
				except:
					donothing=1	
				try:
					os.remove("output2.csv")
				except:
					donothing=1				
				try:
					os.remove("output3.csv")
				except:
					donothing=1
				try:
					os.remove("output4.csv")
				except:
					donothing=1	
				try:
					os.remove("outputtomerge.csv")
				except:
					donothing=1								
				try:
					os.remove("temp.csv")
				except:
					donothing=1
				try:
					os.remove("temp2.csv")
				except:
					donothing=1						
				try:
					os.remove("blankfile1.tmp")
				except:
					donothing=1				
				try:
					os.remove("blankfile2.tmp")
				except:
					donothing=1				

				if success1 == 0 and success2 == 0:
					lines = lines.rstrip()
					outputlog.write(lines + "," + mergedfilename+"\n")
				else:
					outputlog.write(lines + ",\n")

print( "\nSummary:")
print( "Input:")
print( inputlogfile)
print( "Output:")
print( outputlogfile)
for element in mergedfilenamelist:
	print( str(element))


