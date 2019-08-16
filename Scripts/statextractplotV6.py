from pylab import *
from sklearn import linear_model 
import sys, math
import numpy as np
import matplotlib.pyplot as plt
import csv, itertools , xlwt ,operator
import pandas as pd
from collections import OrderedDict
import os
import matplotlib.lines as mlines



importantudp = []
importanttcp = []
pingAvgline = []
supData = []
SupKeyWord_Connect = ["CTRL-EVENT-CONNECTED"]
SupKeyWord_Disconnect = ["CTRL-EVENT-DISCONNECTED"]
BFevent_data = ["BF-EVENT-DATA"]
Link_eventData = ["LINK-EVENT-DATA"]
keep_phrases = ["bits/sec"]
myKeyWord = str("---------------")
pingKeyword = str("rtt min/avg/max")
pingTime = str("time=")
startSupKeyWord = str("PING")
SortingKeyWord = str("Gbits/sec")
SortingKeyWord2 = str("Mbits/sec")
SortingKeyWord3 = str("Kbits/sec")
listPingValue = []
valueAvgUdp = float()
valueAvgTcp = float()
avgPing = float()
sumData1 = float()
sumData2 = float()
sumData3 = float()
startSup = None
endSup = None
listxaxis2 = []
startOffFrom = 2 # second
TimeStampConnectedStart = []
TimeStampDisconnectedEnd = []
lineconnectedtrue= 0
collectperiodsec= 5
RSSIDataList = []
OUTPUT_FOLDER = "Results/"
OUTPUT_FOLDER2 = "Results/Graphs/"
OUTPUT_FOLDER3 = "Results/Consolidated files/"
OUTPUT_FOLDER4 = "Results/Consolidated files/"
TIMESTAMPLENGTH = 17 # hardcoded!
SKIPFIRSTREADING = 1 # set to 1 to ignore first measurement (note: sometimes first readings are significantly worse)
timestamplist = []
numberofcommas = 6 #Hardcode count number of commas in statsupfile

#Finding total SNR, RemoteSNR and RSSI 
TotalBestBeamSNR = 0
TotalLastRemoteRssi = 0
TotalLastBeaconRssi = 0
TotalLastDataRssi = 0
TotalCurrentMcs = 0
TotalRFTemp = 0
TotalBBTemp = 0


TotalBestBeamSNR2 = 0
TotalLastRemoteRssi2 = 0
TotalLastBeaconRssi2 = 0
TotalLastDataRssi2 = 0
TotalCurrentMcs2 = 0
TotalRFTemp2 = 0
TotalBBTemp2 = 0

stateventdatakeyword = ["STATS-EVENT-DATA:"]
#filterword = ["FAIL"]

BestBeamSNRDataList = []
LastRemoteRssiDataList = []
LastBeaconRssiDataList = []
LastDataRssiDataList = []
CurrentMcsDataList = []
RFTempDataList = []
BBTempDataList = []

def twos_comp(val, bits): #"""compute the 2's complement of int value val"""
	if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
		val = val - (1 << bits)        # compute negative value
	return val                         # return positive value as is


def hex_to_dex(strng_of_hex):
	return int(strng_of_hex, 16)

## main
print( "INFO: START EXTRACT PLOT\n")

# Get log file name and check if valid
if len(sys.argv) != 2:
	print( "Correct usage: python extractplot<ver>.py [dir]/[filename].csv")
	quit() # not valid so exit

if SKIPFIRSTREADING  == 1:
	print( "Note: Skip first reading: Enabled (to avoid abnormal values)")

inputlogfile = sys.argv[1]
# inputlogfiledir = os.path.dirname(os.path.realpath(inputlogfile)) + "/"
inputlogfiledir = str(inputlogfile.rsplit('/',1)[0]) + "/"
inputlogfilename = os.path.basename(inputlogfile)

outputextractstatsup = inputlogfiledir+OUTPUT_FOLDER+"output_stat_"+inputlogfilename
outputextractstatsupsorted = inputlogfiledir+OUTPUT_FOLDER+"output_sorted_stat_"+inputlogfilename
outputextractstatsupsortedmerged = inputlogfiledir+OUTPUT_FOLDER3+"output_sortedmerged_stat_"+inputlogfilename
#outputextractperf = inputlogfiledir+OUTPUT_FOLDER+"output_perf_"+inputlogfilename
#outputextractperfsorted = inputlogfiledir+OUTPUT_FOLDER+"output_sorted_perf_"+inputlogfilename
outputextractperfsortedmerged = inputlogfiledir+OUTPUT_FOLDER4+"output_sortedmerged_perf_"+inputlogfilename
outputextractstatsupperfsortedmerged = inputlogfiledir+OUTPUT_FOLDER+"output_sortedmerged_statperf_"+inputlogfilename

outputextractsupstatsupperfsortedmerged = inputlogfiledir+OUTPUT_FOLDER3+"output_sortedmerged_supstatperf_"+inputlogfilename

outputextractsupperfsortedmerged = inputlogfiledir+OUTPUT_FOLDER+"output_sortedmerged_supperf_"+inputlogfilename #Extracting sup data from summarised sup perf file data

#Creates empty files
statsupfile = open(outputextractstatsup, "w")
statsupfile.close()
statsupsortedfile = open(outputextractstatsupsorted, "w")
statsupsortedfile.close()
supsortedmergedfile = open(outputextractstatsupsortedmerged, "w")
supsortedmergedfile.close()
#perffile = open(outputextractperf, "w")
#perffile.close()
#perfsortedfile = open(outputextractperfsorted, "w")
#perfsortedfile.close()
#perfsortedmergedfile = open(outputextractperfsortedmerged, "w")
#perfsortedmergedfile.close()
# supperfsortedmergedfile = open(outputextractstatupperfsortedmerged, "w")
# supperfsortedmergedfile.close()

print( "\nSummary:")
print( "Input:")
print( inputlogfile)
print( "Output:")
#print( outputextractstatsup
# print( outputextractstatsupsorted
print( outputextractstatsupsortedmerged)
# print( outputextractperf
# print( outputextractperfsorted
print( outputextractperfsortedmerged)
print( outputextractstatsupperfsortedmerged)
print( outputextractsupstatsupperfsortedmerged)

#Creating headers
with open(outputextractstatsup, "w") as supfile:
	writer4 = csv.DictWriter(supfile, fieldnames = ["Distance", "BestBeamSNR", "Average BestBeamSNR", "LastRemoteRssi", "Average LastRemoteRssi",  "LastBeaconRssi", "Average LastBeaconRssi" , "LastDataRssi" , "Average LastDataRssi" , "CurrentMcs" , "Frequent CurrentMcs" , "RFTemp" , "Average RFTemp", "BBTemp", "Average BBTemp"], delimiter = ',' )
	writer4.writeheader()
supfile.close()

with open(outputextractstatsupsortedmerged, "w") as supsortedmergedfile:
	writer4 = csv.DictWriter(supsortedmergedfile, fieldnames = ["Distance","BestBeamSNR", "Average BestBeamSNR", "LastRemoteRssi", "Average LastRemoteRssi",  "LastBeaconRssi", "Average LastBeaconRssi" , "LastDataRssi" , "Average LastDataRssi" , "CurrentMcs" , "Frequent CurrentMcs" , "RFTemp" , "Average RFTemp", "BBTemp", "Average BBTemp"], delimiter = ',' )
	writer4.writeheader()
supsortedmergedfile.close()

# with open(outputextractperfsortedmerged, "wb") as perfsortedmergedfile:
# 	writer2 = csv.DictWriter(perfsortedmergedfile, fieldnames = ["Distance", "Ping Values", "Avg Ping Values", "Udp Values",  "Avg Udp Values", "Tcp Values" , "Avg Tcp Values"], delimiter = ',' )
# 	writer2.writeheader()
# perfsortedmergedfile.close()

# #Assigns header to each file
# with open(outputextractperf, "a") as perffile: #Change file name here
# 	writer = csv.DictWriter(perffile, fieldnames = ["Distance", "Ping Values", "Avg Ping Values", "Udp Values",  "Avg Udp Values", "Tcp Values" , "Avg Tcp Values"], delimiter = ',' )
# 	writer.writeheader()
# perffile.close()

with open(outputextractstatsupperfsortedmerged, "w") as supperfsortedmergedfile:
	writer5 = csv.DictWriter(supperfsortedmergedfile, fieldnames = ["Distance","Average BestBeamSNR","Average LastRemoteRssi","Average LastBeaconRssi" , "Average LastDataRssi" ,"Frequent CurrentMcs" ,"Average RFTemp","Average BBTemp", "Average Ping" , "Average Udp", "Average Tcp"], delimiter = ',' )
	writer5.writeheader()
supperfsortedmergedfile.close()

with open(outputextractsupstatsupperfsortedmerged, "w") as supstatsupperfsortedmergedfile:
	writer6 = csv.DictWriter(supstatsupperfsortedmergedfile, fieldnames = ["Distance","Average BestBeamSNR","Average LastRemoteRssi","Average LastBeaconRssi" , "Average LastDataRssi" ,"Frequent CurrentMcs" ,"Average RFTemp","Average BBTemp", "Average Ping" , "Average Udp", "Average Tcp","Frequent TxSectorData","Frequent RxSectorData","Average SNRData Div 8" ,"Average RemoteSNRData Div 8" ,"Average RSSIData"], delimiter = ',' )
	writer6.writeheader()
supstatsupperfsortedmergedfile.close()



#Code: plots latest data collected from each file
with open(inputlogfile, "rt") as inputlog: #Input main file name
	inputlogcontent = inputlog.readlines()[1:]
	for line in inputlogcontent:

		xaxis = float(line.split(",")[2]) #find x axis
		udpFilePathName = inputlogfiledir + str(line.split(",")[11]) #find udp files

		tcpFilePathName = inputlogfiledir + str(line.split(",")[12]) #find tcp files
	
		statsupFilePathName = inputlogfiledir + str(line.split(",")[14]) #find stat files

		# print( udpFilePathName
		# print( pingFilePathName
		# print( tcpFilePathName
		# print( supFilePathName


		print( "INFO: PROCESSING SUP FILE\n")


############## Determine Earliest and Latest Timestamp of UDP and TCP for extracting supplicant ##################################

		noudpfile=0
		notcpfile=0

		try:
			with open(udpFilePathName ,"r") as udpfile:
					#firstlineudp = udpfile.readlines()
				lastlineudp = udpfile.readlines()[-1]
				lastlineudptimestamp = str(lastlineudp).split(" ")[0]
				timestamplist = timestamplist + [lastlineudptimestamp]
			udpfile.close()

			with open(udpFilePathName ,"r") as udpfile:
				firstlineudp = udpfile.readlines()[1]
				firstlineudptimestamp = str(firstlineudp).split(" ")[0]
				#lastlineudp = udpfile.readlines()[-1]
				timestamplist = timestamplist + [firstlineudptimestamp]
			udpfile.close()
		except:
			noudpfile=1

		try:	
			with open(tcpFilePathName, "r") as tcpfile:
				firstlinetcp = tcpfile.readlines()[1]
				firstlinetcptimestamp = str(firstlinetcp).split(" ")[0]
				timestamplist = timestamplist + [firstlinetcptimestamp]
			tcpfile.close()

			with open(tcpFilePathName, "r") as tcpfile:
				lastlinetcp = tcpfile.readlines()[-1]
				lastlinetcptimestamp = str(lastlinetcp).split(" ")[0]
				timestamplist = timestamplist + [lastlinetcptimestamp]
			tcpfile.close()
		except:
			notcpfile=1

		if(noudpfile==1 and notcpfile==1):
			earliesttimestamp = 999999999999999999	# Set to extremely large value so that sup file is not read
			latesttimestamp = earliesttimestamp
		else:
			earliesttimestamp = min(str(s) for s in timestamplist)
			latesttimestamp = max(str(s) for s in timestamplist)

		#clear timestamplist to prevent repeat
		timestamplist = []

############################################################################


		# Note: assumed that sup file always exists and not empty
		with open(statsupFilePathName, "rt") as statSupFile:
			#print( statsupFilePathName
			statSupFilelines = statSupFile.readlines()

			# lineconnectedtrue= 0
			for line in statSupFilelines:
				#print(  line
				TimestampLine = line.split(" ")[0]
				if len(TimestampLine) != TIMESTAMPLENGTH:
					donothing = 1
					#print( "WARNING ("+statsupFilePathName+" has line without timestamp)"
					continue
				
				if float(TimestampLine) >= float(earliesttimestamp) and float(TimestampLine) <= float(latesttimestamp): 
					for phrases in stateventdatakeyword:
						if phrases in line and str("FAIL") not in line and line.count(',') == numberofcommas:
							#print( line
							dataList = line.split(" ")[2]

							BestBeamSNRData = dataList.split(',')[0]
							BestBeamSNRData = hex_to_dex(BestBeamSNRData)
							#print( BestBeamSNRData
							BestBeamSNRData = twos_comp(BestBeamSNRData, 8)
							#print( BestBeamSNRData
							BestBeamSNRDataList = BestBeamSNRDataList + [str(BestBeamSNRData)]
							TotalBestBeamSNR = TotalBestBeamSNR + float(BestBeamSNRData)

							LastRemoteRssiData = dataList.split(',')[1]
							LastRemoteRssiData = hex_to_dex(LastRemoteRssiData)
							LastRemoteRssiData = twos_comp(LastRemoteRssiData , 8)
							LastRemoteRssiDataList = LastRemoteRssiDataList + [str(LastRemoteRssiData)]
							TotalLastRemoteRssi = TotalLastRemoteRssi + float(LastRemoteRssiData)

							LastBeaconRssiData = dataList.split(',')[2]
							#print( LastBeaconRssiData
							LastBeaconRssiData = hex_to_dex(LastBeaconRssiData) 
							LastBeaconRssiData = twos_comp(LastBeaconRssiData, 8)
							LastBeaconRssiDataList = LastBeaconRssiDataList + [str(LastBeaconRssiData)]
							TotalLastBeaconRssi = TotalLastBeaconRssi + float(LastBeaconRssiData)

							LastDataRssiData = dataList.split(',')[3]
							LastDataRssiData = hex_to_dex(LastDataRssiData)
							LastDataRssiData = twos_comp(LastDataRssiData, 8)
							LastDataRssiDataList = LastDataRssiDataList + [str(LastDataRssiData)]
							TotalLastDataRssi = TotalLastDataRssi + float(LastDataRssiData)

							CurrentMcsData = dataList.split(',')[4]
							CurrentMcsData = hex_to_dex(CurrentMcsData)
							CurrentMcsDataList = CurrentMcsDataList + [str(CurrentMcsData)]


							RFTempData = dataList.split(',')[5]
							RFTempData = hex_to_dex(RFTempData)
							RFTempData = twos_comp(RFTempData, 16)
							RFTempDataList = RFTempDataList + [str(RFTempData)]
							TotalRFTemp = TotalRFTemp + float(RFTempData)
						

							BBTempData = dataList.split(',')[6]
							BBTempData =  hex_to_dex(BBTempData)
							BBTempData = twos_comp(BBTempData, 160)
							BBTempDataList = BBTempDataList + [str(BBTempData)]
							TotalBBTemp = TotalBBTemp + float(BBTempData)
	



# get counts for each unique value
			if (len(BestBeamSNRDataList)>0):

				a = BestBeamSNRDataList 
				aCount = {x:a.count(x) for x in a}
				#valuesA = sorted(aCount.values())
				countA = sorted(aCount, key=aCount.get)
				mostFrequentBestBeamSNRData = countA[-1]

				BestBeamSNRDataListLength = len(BestBeamSNRDataList)
				AverageBestBeamSNRData = TotalBestBeamSNR / BestBeamSNRDataListLength

	# sort list in ascending order
				BestBeamSNRDataCountSorted = sorted(aCount.items(), key = lambda x:int(x[0]))



	#formats everthing
				BestBeamSNRDataCountFormatted = str(BestBeamSNRDataCountSorted).strip('[]')
				BestBeamSNRDataCountFormatted = BestBeamSNRDataCountFormatted.replace("('","")
				BestBeamSNRDataCountFormatted = BestBeamSNRDataCountFormatted.replace("', ","(")
				BestBeamSNRDataCountFormatted = BestBeamSNRDataCountFormatted.replace(",","")


			else:
				BestBeamSNRDataCountFormatted=""

#Steps repeated for rest of RxSector, SNR, RemoteSNR, RRSI
			if (len(LastRemoteRssiDataList)>0):

				b = LastRemoteRssiDataList
				bCount = {xx:b.count(xx) for xx in b}
				countB = sorted(bCount, key=bCount.get)
				mostFrequentLastRemoteRssiData = countB[-1]

				LastRemoteRssiDataListLength = len(LastRemoteRssiDataList)
				AverageLastRemoteRssiData = TotalLastRemoteRssi / LastRemoteRssiDataListLength

				LastRemoteRssiDataCountSorted = sorted(bCount.items(), key = lambda x:int(x[0]))

				LastRemoteRssiDataCountFormatted = str(LastRemoteRssiDataCountSorted).strip('[]')
				LastRemoteRssiDataCountFormatted = LastRemoteRssiDataCountFormatted.replace("('","")
				LastRemoteRssiDataCountFormatted = LastRemoteRssiDataCountFormatted.replace("', ","(")
				LastRemoteRssiDataCountFormatted = LastRemoteRssiDataCountFormatted.replace(",","")
			else:
				LastRemoteRssiDataCountFormatted=""

			if (len(LastBeaconRssiDataList)>0):

				c = LastBeaconRssiDataList
				cCount = {xxx:c.count(xxx) for xxx in c}
				countC = sorted(cCount, key=cCount.get)
				mostFrequentLastBeaconRssi = countC[-1]

				LastBeaconRssiDataListLength = len(LastBeaconRssiDataList)
				AverageLastBeaconRssiData = TotalLastBeaconRssi / LastBeaconRssiDataListLength


				LastBeaconRssiDataCountSorted = sorted(cCount.items(), key = lambda x:int(x[0]))

				LastBeaconRssiDataCountFormatted = str(LastBeaconRssiDataCountSorted).strip('[]')
				LastBeaconRssiDataCountFormatted = LastBeaconRssiDataCountFormatted.replace("('","")
				LastBeaconRssiDataCountFormatted = LastBeaconRssiDataCountFormatted.replace("', ","(")
				LastBeaconRssiDataCountFormatted = LastBeaconRssiDataCountFormatted.replace(",","")
			else:
				SNRDataDataCountFormatted=""

			if (len(LastDataRssiDataList)>0):

				d = LastDataRssiDataList
				dCount = {xxxx:d.count(xxxx) for xxxx in d}
				countD = sorted(dCount, key=dCount.get)
				mostFrequentLastDataRssi = countD[-1]

				LastDataRssiDataListLength = len(LastDataRssiDataList)
				AverageLastDataRssiData = TotalLastDataRssi / LastDataRssiDataListLength


				LastDataRssiDataCountSorted = sorted(dCount.items(), key = lambda x:int(x[0]))

				LastDataRssiDataCountFormatted = str(LastDataRssiDataCountSorted).strip('[]')
				LastDataRssiDataCountFormatted = LastDataRssiDataCountFormatted.replace("('","")
				LastDataRssiDataCountFormatted = LastDataRssiDataCountFormatted.replace("', ","(")
				LastDataRssiDataCountFormatted = LastDataRssiDataCountFormatted.replace(",","")
			else:
				LastDataRssiDataCountFormatted=""

			if (len(CurrentMcsDataList)>0):

				e = CurrentMcsDataList
				eCount = {xxxxx:e.count(xxxxx) for xxxxx in e}
				countE = sorted(eCount, key=eCount.get)
				mostFrequentCurrentMcsData = countE[-1]

				CurrentMcsDataListLength = len(CurrentMcsDataList)
				AverageCurrentMcsData = TotalCurrentMcs / CurrentMcsDataListLength

				CurrentMcsDataCountSorted = sorted(eCount.items(), key = lambda x:int(x[0]))

				CurrentMcsDataCountFormatted = str(CurrentMcsDataCountSorted).strip('[]')
				CurrentMcsDataCountFormatted = CurrentMcsDataCountFormatted.replace("('","")
				CurrentMcsDataCountFormatted = CurrentMcsDataCountFormatted.replace("', ","(")
				CurrentMcsDataCountFormatted = CurrentMcsDataCountFormatted.replace(",","")
			else:
				CurrentMcsDataCountFormatted=""

			if (len(RFTempDataList)>0):

				f = RFTempDataList
				fCount = {xxxxxx:f.count(xxxxxx) for xxxxxx in f}
				countF = sorted(fCount, key=fCount.get)
				mostFrequentRFTemp = countF[-1]

				RFTempDataListLength = len(RFTempDataList)
				AverageRFTempData = TotalRFTemp / RFTempDataListLength
	


				RFTempDataCountSorted = sorted(fCount.items(), key = lambda x:int(x[0]))

				RFTempDataCountFormatted = str(RFTempDataCountSorted).strip('[]')
				RFTempDataCountFormatted = RFTempDataCountFormatted.replace("('","")
				RFTempDataCountFormatted = RFTempDataCountFormatted.replace("', ","(")
				RFTempDataCountFormatted = RFTempDataCountFormatted.replace(",","")

			else:
				RFTempDataCountFormatted=""

			if (len(BBTempDataList)>0):

				g = BBTempDataList
				gCount = {xxxxxxx:g.count(xxxxxxx) for xxxxxxx in g}
				countG = sorted(gCount, key=gCount.get)
				mostFrequentBBTempData = countG[-1]

				BBTempDataListLength = len(BBTempDataList)
				AverageBBTempData = TotalBBTemp / BBTempDataListLength


				BBTempDataCountSorted = sorted(gCount.items(), key = lambda x:int(x[0]))

				BBTempDataCountFormatted = str(BBTempDataCountSorted).strip('[]')
				BBTempDataCountFormatted = BBTempDataCountFormatted.replace("('","")
				BBTempDataCountFormatted = BBTempDataCountFormatted.replace("', ","(")
				BBTempDataCountFormatted = BBTempDataCountFormatted.replace(",","")

			else:
				BBTempDataCountFormatted=""

			BestBeamSNRDataList = []
			LastRemoteRssiDataList = []
			LastBeaconRssiDataList = []
			LastDataRssiDataList = []
			CurrentMcsDataList = []
			RFTempDataList = []
			BBTempDataList = []

			TotalBestBeamSNR = 0.0
			TotalLastRemoteRssi = 0.0
			TotalLastBeaconRssi = 0.0
			TotalLastDataRssi = 0.0
			TotalCurrentMcs = 0.0
			TotalRFTemp = 0.0
			TotalBBTemp = 0.0

			#Creates CSV file

			with open(outputextractstatsup, "a") as statsupfile: #Change file name here
				statsupfile.write(str(xaxis) +","+ BestBeamSNRDataCountFormatted + "," + str(AverageBestBeamSNRData) + "," + LastRemoteRssiDataCountFormatted + "," + str(AverageLastRemoteRssiData)  + "," + LastBeaconRssiDataCountFormatted + "," + str(AverageLastBeaconRssiData) + "," + LastDataRssiDataCountFormatted + "," + str(AverageLastDataRssiData) + "," + CurrentMcsDataCountFormatted + "," + str(mostFrequentCurrentMcsData) + "," + RFTempDataCountFormatted+ "," + str(AverageRFTempData) + "," + BBTempDataCountFormatted+ "," + str(AverageBBTempData) + "\n")
			statsupfile.close()		



#Merge data (sup) based on distacce (every distance only have 1 row) - save as different file ; orig, sorted, merge sorted file 

print( "INFO: SORT AND MERGE SUP\n")


#Opens output file and sorts according to distance
with open(outputextractstatsup , 'r') as data:
	data = csv.reader(data,delimiter=',')
	next(data)
	list1 = sorted(data, key=lambda x: (float(x[0])))

#Creates new file "output_sorted"
with open(outputextractstatsupsorted, "w") as f:
	fileWriter = csv.writer(f, delimiter=',')
	writer = csv.DictWriter(f, fieldnames = ["Distance", "BestBeamSNR", "Average BestBeamSNR", "LastRemoteRssi", "Average LastRemoteRssi",  "LastBeaconRssi", "Average LastBeaconRssi" , "LastDataRssi" , "Average LastDataRssi" , "CurrentMcs" , "Frequent CurrentMcs" , "RFTemp" , "Average RFTemp", "BBTemp", "Average BBTemp"], delimiter = ',' )
	writer.writeheader()
	for row in list1:
		fileWriter.writerow(row)
f.close()

#Stat merging same distances (sup)

with open(outputextractstatsupsorted, "r") as merge1sup:
	merge1linessup = merge1sup.readlines()[1:]
	merge2linessup = merge1linessup

merge1Index = -1
merge1NextIndex = 1

BestBeamSNRDataList = []
LastRemoteRssiDataList = []
LastBeaconRssiDataList = []
LastDataRssiDataList = []
CurrentMcsDataList = []
RFTempDataList = []
BBTempDataList = []

for line in merge1linessup:
	merge1Index = merge1Index+1
	combineFlag = 0
	if merge1Index == 0 or merge1Index == merge1NextIndex:
		merge2Index = -1		
		merge1col = line.split(',')[0]
		for line2 in merge2linessup:
			merge2Index = merge2Index + 1
			merge2col = line2.split(',')[0]

			if merge2Index > merge1Index: #starting one more than previous 
#Data is matched and merged if equal
				if merge1col == merge2col:		
					combineFlag = 1
#Find new average BestBeamSNR
					bestbeamsnrData = line.split(',')[1] + " " + line2.split(',')[1]
					bestbeamsnrData = bestbeamsnrData.split()
					lenbestbeamsnrData = len(bestbeamsnrData)

					# Expand values then compress after
					for element in bestbeamsnrData:
						bestbeamsnrDataval = element.split('(')[0]
						bestbeamsnrDatavalcount = int(element.split('(')[1].split(')')[0])
						for index_i in range(bestbeamsnrDatavalcount):
							BestBeamSNRDataList.append(bestbeamsnrDataval)

					a = BestBeamSNRDataList
					
					bestbeamsnrDatalistlength = len(BestBeamSNRDataList)

					for elements in BestBeamSNRDataList:
						TotalBestBeamSNR2 = TotalBestBeamSNR2 + float(elements)
					AverageBestBeamSNRData2 = TotalBestBeamSNR2 / bestbeamsnrDatalistlength
		

					aCount = {x:a.count(x) for x in a}
					countA = sorted(aCount, key=aCount.get)
					mostFrequentBestBeamSNRData = countA[-1]

					BestBeamSNRDataCountSorted = sorted(aCount.items(), key = lambda x:int(x[0]))

					#formats everthing
					BestBeamSNRDataCountFormatted = str(BestBeamSNRDataCountSorted).strip('[]')
					BestBeamSNRDataCountFormatted = BestBeamSNRDataCountFormatted.replace("('","")
					BestBeamSNRDataCountFormatted = BestBeamSNRDataCountFormatted.replace("', ","(")
					BestBeamSNRDataCountFormatted = BestBeamSNRDataCountFormatted.replace(",","")



#Steps repeated for rest of LastRemoteRssi,LastBeaconRssi,LastDataRssi,CurrentMcs,RFTemp,BBTemp

#Find new frequent for LastRemoteRssiData
					lastremoterssiData = line.split(',')[3] + " " + line2.split(',')[3]
					lastremoterssiData = lastremoterssiData.split()
					lenlastremoterssiData = len(lastremoterssiData)

					# Expand values then compress after
					for element in lastremoterssiData:
						lastremoterssiDataval = element.split('(')[0]
						lastremoterssiDatavalcount = int(element.split('(')[1].split(')')[0])
						for index_i in range(lastremoterssiDatavalcount):
							LastRemoteRssiDataList.append(lastremoterssiDataval)

					b = LastRemoteRssiDataList

					lastremoterssiDatalistlength = len(LastRemoteRssiDataList)

					for elements in LastRemoteRssiDataList:
						TotalLastRemoteRssi2 = TotalLastRemoteRssi2 + float(elements)
					AverageLastRemoteRssiData2 = TotalLastRemoteRssi2 /lastremoterssiDatalistlength


					bCount = {xx:b.count(xx) for xx in b}
					countB = sorted(bCount, key=bCount.get)
					mostFrequentLastRemoteRssiData = countB[-1]

					LastRemoteRssiDataCountSorted = sorted(bCount.items(), key = lambda x:int(x[0]))

					LastRemoteRssiDataCountFormatted = str(LastRemoteRssiDataCountSorted).strip('[]')
					LastRemoteRssiDataCountFormatted = LastRemoteRssiDataCountFormatted.replace("('","")
					LastRemoteRssiDataCountFormatted = LastRemoteRssiDataCountFormatted.replace("', ","(")
					LastRemoteRssiDataCountFormatted = LastRemoteRssiDataCountFormatted.replace(",","")

#Find new average for LastBeaconRssiData
					lastbeaconrssiData = line.split(',')[5] + " " + line2.split(',')[5]
					lastbeaconrssiData = lastbeaconrssiData.split()
					lenlastbeaconrssiData = len(lastbeaconrssiData)


					# Expand values then compress after
					for element in lastbeaconrssiData:
						lastbeaconrssiDataval = element.split('(')[0]
						lastbeaconrssiDatavalcount = int(element.split('(')[1].split(')')[0])
						for index_i in range(lastbeaconrssiDatavalcount):
							LastBeaconRssiDataList.append(lastbeaconrssiDataval)

					c = LastBeaconRssiDataList

					lastbeaconrssiDatalistlength = len(LastBeaconRssiDataList)

					for elements in LastBeaconRssiDataList:
						TotalLastBeaconRssi2 = TotalLastBeaconRssi2 + float(elements)
					AverageLastBeaconRssiData2 = TotalLastBeaconRssi2 /lastbeaconrssiDatalistlength

					cCount = {xxx:c.count(xxx) for xxx in c}
					countC = sorted(cCount, key=cCount.get)
					mostFrequentLastBeaconRssi = countC[-1]

					LastBeaconRssiDataCountSorted = sorted(cCount.items(), key = lambda x:int(x[0]))

					LastBeaconRssiDataCountFormatted = str(LastBeaconRssiDataCountSorted).strip('[]')
					LastBeaconRssiDataCountFormatted = LastBeaconRssiDataCountFormatted.replace("('","")
					LastBeaconRssiDataCountFormatted = LastBeaconRssiDataCountFormatted.replace("', ","(")
					LastBeaconRssiDataCountFormatted = LastBeaconRssiDataCountFormatted.replace(",","")

#Find new average for LastDataRssi
					lastdatarssiData = line.split(',')[7] + " " + line2.split(',')[7]
					lastdatarssiData = lastdatarssiData.split()
					lenlastdatarssiData = len(lastdatarssiData)

					# Expand values then compress after
					for element in lastdatarssiData:
						lastdatarssiDataval = element.split('(')[0]
						lastdatarssiDatavalcount = int(element.split('(')[1].split(')')[0])
						for index_i in range(lastdatarssiDatavalcount):
							LastDataRssiDataList.append(lastdatarssiDataval)

					d = LastDataRssiDataList

					lastdatarssiDatalistlength = len(LastDataRssiDataList)

					for elements in LastDataRssiDataList:
						TotalLastDataRssi2 = TotalLastDataRssi2 + float(elements)
					AverageLastDataRssiData2 = TotalLastDataRssi2 /lastdatarssiDatalistlength


					dCount = {xxxx:d.count(xxxx) for xxxx in d}
					countD = sorted(dCount, key=dCount.get)
					mostFrequentLastDataRssi = countD[-1]

					LastDataRssiDataCountSorted = sorted(dCount.items(), key = lambda x:int(x[0]))

					LastDataRssiDataCountFormatted = str(LastDataRssiDataCountSorted).strip('[]')
					LastDataRssiDataCountFormatted = LastDataRssiDataCountFormatted.replace("('","")
					LastDataRssiDataCountFormatted = LastDataRssiDataCountFormatted.replace("', ","(")
					LastDataRssiDataCountFormatted = LastDataRssiDataCountFormatted.replace(",","")

#Find new most frequent for CurrentMcs
					currentmcsData = line.split(',')[9] + " " + line2.split(',')[9]
					currentmcsData = currentmcsData.split()
					lencurrentmcsData = len(currentmcsData)

					# Expand values then compress after
					for element in currentmcsData:
						currentmcsDataval = element.split('(')[0]
						currentmcsDatavalcount = int(element.split('(')[1].split(')')[0])
						for index_i in range(currentmcsDatavalcount):
							CurrentMcsDataList.append(currentmcsDataval)

					e = CurrentMcsDataList



					currentmcsDatalistlength = len(CurrentMcsDataList)

					for elements in CurrentMcsDataList:
						TotalCurrentMcs2 = TotalCurrentMcs2 + float(elements)
					AverageCurrentMcsData2 = TotalCurrentMcs2 / currentmcsDatalistlength

					eCount = {xxxxx:e.count(xxxxx) for xxxxx in e}
					countE = sorted(eCount, key=eCount.get)
					mostFrequentCurrentMcs = countE[-1]

					CurrentMcsDataCountSorted = sorted(eCount.items(), key = lambda x:int(x[0]))
					CurrentMcsDataCountFormatted = str(CurrentMcsDataCountSorted).strip('[]')
					CurrentMcsDataCountFormatted = CurrentMcsDataCountFormatted.replace("('","")
					CurrentMcsDataCountFormatted = CurrentMcsDataCountFormatted.replace("', ","(")
					CurrentMcsDataCountFormatted = CurrentMcsDataCountFormatted.replace(",","")

	

#Find new average for RFTemp
					rftempData = line.split(',')[11] + " " + line2.split(',')[11]
					rftempData = rftempData.split()
					lenrftempData = len(rftempData)

					# Expand values then compress after
					for element in rftempData:
						rftempDataval = element.split('(')[0]
						rftempDatavalcount = int(element.split('(')[1].split(')')[0])
						for index_i in range(rftempDatavalcount):
							RFTempDataList.append(rftempDataval)

					f = RFTempDataList

					rftempDatalistlength = len(RFTempDataList)

					for elements in RFTempDataList:
						TotalRFTemp2 = TotalRFTemp2 + float(elements)
					AverageRFTemp2 = TotalRFTemp2 / rftempDatalistlength

					fCount = {xxxxx:f.count(xxxxx) for xxxxx in f}
					countF = sorted(fCount, key=fCount.get)
					mostFrequentRFTempData = countF[-1]

					RFTempDataCountSorted = sorted(fCount.items(), key = lambda x:int(x[0]))


					RFTempDataCountFormatted = str(RFTempDataCountSorted).strip('[]')
					RFTempDataCountFormatted = RFTempDataCountFormatted.replace("('","")
					RFTempDataCountFormatted = RFTempDataCountFormatted.replace("', ","(")
					RFTempDataCountFormatted = RFTempDataCountFormatted.replace(",","")
		
	

#Find new average for BBTemp
					bbtempData = line.split(',')[13] + " " + line2.split(',')[13]
					bbtempData = bbtempData.split()
					lenbbtempData = len(bbtempData)

					# Expand values then compress after
					for element in bbtempData:
						bbtempDataval = element.split('(')[0]
						bbtempDatavalcount = int(element.split('(')[1].split(')')[0])
						for index_i in range(bbtempDatavalcount):
							BBTempDataList.append(bbtempDataval)

					g = BBTempDataList


					bbtempDatalistlength = len(BBTempDataList)

					for elements in BBTempDataList:
						TotalBBTemp2 = TotalBBTemp2 + float(elements)
					AverageBBTemp2 = TotalBBTemp2 / bbtempDatalistlength

					gCount = {xxxxx:g.count(xxxxx) for xxxxx in g}
					countG = sorted(gCount, key=gCount.get)
					mostFrequentBBTempData = countG[-1]

					BBTempDataCountSorted = sorted(gCount.items(), key = lambda x:int(x[0]))

					BBTempDataCountFormatted = str(BBTempDataCountSorted).strip('[]')
					BBTempDataCountFormatted = BBTempDataCountFormatted.replace("('","")
					BBTempDataCountFormatted = BBTempDataCountFormatted.replace("', ","(")
					BBTempDataCountFormatted = BBTempDataCountFormatted.replace(",","")



					TotalBestBeamSNR2 = 0
					TotalLastRemoteRssi2 = 0
					TotalLastBeaconRssi2 = 0
					TotalLastDataRssi2 = 0
					TotalCurrentMcs2 = 0
					TotalRFTemp2 = 0
					TotalBBTemp2 = 0


# #Putting everthing into a new line
					Newline = line.split(',')[0] + ','+ BestBeamSNRDataCountFormatted + "," + str(AverageBestBeamSNRData2) + "," + LastRemoteRssiDataCountFormatted + "," + str(AverageLastRemoteRssiData2) + "," + LastBeaconRssiDataCountFormatted + "," + str(AverageLastBeaconRssiData2) + "," + LastDataRssiDataCountFormatted + "," + str(AverageLastDataRssiData2) + "," + CurrentMcsDataCountFormatted + "," + mostFrequentCurrentMcs + "," + RFTempDataCountFormatted + "," + str(AverageRFTemp2) + "," + BBTempDataCountFormatted + "," + str(AverageBBTemp2) + "\n"
					merge1NextIndex = merge2Index+1

					#Resets list
					BestBeamSNRDataList = []
					LastRemoteRssiDataList = []
					LastBeaconRssiDataList = []
					LastDataRssiDataList = []
					CurrentMcsDataList = []
					RFTempDataList = []
					BBTempDataList = []



# #print(s existing data from line1 if not equal (no merge)
				else :			
					if combineFlag == 0: #Prevents  Newline from overide
						Newline = line
					merge1NextIndex = merge2Index				
					break		

#Gets data for first and last distance "Corner cases"
			else: 
				if merge1Index == 0 or merge2Index == len(merge2linessup)-1:  #i.e first line or last line
					if combineFlag == 0:
						Newline = line
						#Resets list
						BestBeamSNRDataList = []
						LastRemoteRssiDataList = []
						LastBeaconRssiDataList = []
						LastDataRssiDataList = []
						CurrentMcsDataList = []
						RFTempDataList = []
						BBTempDataList = []

		
		with open(outputextractstatsupsortedmerged, "a") as supsortedmergedfile:
			supsortedmergedfile.write(Newline)
		supsortedmergedfile.close()


print( "INFO: SORT AND MERGE SUP WITH PERF (SUMMARY)\n")
# Combine sup and perf output files and keep only avg/freq values
with open(outputextractstatsupsortedmerged, "r") as outputsupfile:
	outputsuplines = outputsupfile.readlines()[1:]
outputsupfile.close()

with open(outputextractperfsortedmerged, "r") as outputperffile:
	outputperflines = outputperffile.readlines()[1:]
outputperffile.close()

intermediatelist=[]

with open(outputextractstatsupperfsortedmerged, "a") as outputsupperffile:	
	for index_i in range(len(outputsuplines)):		
		intermediatelist.append(outputsuplines[index_i][:-2].split(',')+outputperflines[index_i][:-2].split(',')) #note: -2 to remove \r\n

		## remove unneeded columns
		intermediatelist[index_i].pop(20)
		intermediatelist[index_i].pop(18)
		intermediatelist[index_i].pop(16)
		intermediatelist[index_i].pop(15)
		intermediatelist[index_i].pop(13)
		intermediatelist[index_i].pop(11)
		intermediatelist[index_i].pop(9)
		intermediatelist[index_i].pop(7)
		intermediatelist[index_i].pop(5)
		intermediatelist[index_i].pop(3)
		intermediatelist[index_i].pop(1)

		intermediatestring = str(intermediatelist[index_i])+"\n"
		intermediatestring = intermediatestring.strip('[')
		intermediatestring = intermediatestring.replace(']',"")
		intermediatestring = intermediatestring.replace("'","")
		outputsupperffile.write(intermediatestring)
outputsupperffile.close()


print( "INFO: SORT AND MERGE STATSUP WITH PERF WITH SUP (SUMMARY)\n")
# Combine sup and perf output files and keep only avg/freq values
with open(outputextractstatsupperfsortedmerged, "r") as outputsupfile1:
	outputsuplines1 = outputsupfile1.readlines()[1:]
outputsupfile1.close()

with open(outputextractsupperfsortedmerged, "r") as outputperffile1:
	outputperflines1 = outputperffile1.readlines()[1:]
outputperffile1.close()

intermediatelist=[]

with open(outputextractsupstatsupperfsortedmerged, "a") as outputsupperffile1:	
	for index_i in range(len(outputsuplines1)):		
		intermediatelist.append(outputsuplines1[index_i][:-2].split(',')+outputperflines1[index_i][:-2].split(',')) #note: -2 to remove \r\n

		## remove unneeded columns
		intermediatelist[index_i].pop(19)
		intermediatelist[index_i].pop(18)
		intermediatelist[index_i].pop(17)
		intermediatelist[index_i].pop(11)
		# intermediatelist[index_i].pop(18)
		# intermediatelist[index_i].pop(16)
		# intermediatelist[index_i].pop(15)
		# intermediatelist[index_i].pop(13)
		# intermediatelist[index_i].pop(11)
		# intermediatelist[index_i].pop(9)
		# intermediatelist[index_i].pop(7)
		#intermediatelist[index_i].pop(5)
		#intermediatelist[index_i].pop(3)
		#intermediatelist[index_i].pop(1)

		intermediatestring = str(intermediatelist[index_i])+"\n"
		intermediatestring = intermediatestring.strip('[')
		intermediatestring = intermediatestring.replace(']',"")
		intermediatestring = intermediatestring.replace("'","")
		outputsupperffile1.write(intermediatestring)

outputsupperffile1.close()

#Creating lists for other plots
BestBeamSNRDataList3 = []
BestBeamSNRDataMostAvgPlotlist = []
LastRemoteRssiDataList3 = []
LastRemoteRssiDataMostAvgPlotlist = []
LastBeaconRssiDataList3 = []
LastBeaconRssiDataMostAvgPlotlist = []
LastDataRssiDataList3 = []
LastDataRssiDataMostAvgPlotlist = []
CurrentMcsDataList3 = []
CurrentMcsDataMostAvgPlotlist = []
RFTempDataList3 = []
RFTempDataMostAvgPlotlist = []
BBTempDataList3 = []
BBTempDataMostAvgPlotlist = []



print( "INFO: GRAPHING SUP\n")

for line in outputsuplines:
	xaxisGraph = line.split(',')[0]
	listxaxis2 = listxaxis2 + [xaxisGraph]

	#Getting Data for TxSector
	BestBeamSNRData = line.split(',')[1]
	BestBeamSNRData = BestBeamSNRData.split()
	lenBestBeamSNRData = len(BestBeamSNRData)
	BestBeamSNRDataMostAvgPlot = line.split(',')[2]
	BestBeamSNRDataMostAvgPlotlist = BestBeamSNRDataMostAvgPlotlist + [BestBeamSNRDataMostAvgPlot]

	# Expand values 
	for element in BestBeamSNRData:
		BestBeamSNRDataval = element.split('(')[0]
		BestBeamSNRDatavalcount = int(element.split('(')[1].split(')')[0])
		for index_i in range(BestBeamSNRDatavalcount):
			BestBeamSNRDataList3.append(BestBeamSNRDataval)


	BestBeamSNRDataList3len = len(BestBeamSNRDataList3)


	plotDistance5 = np.zeros(BestBeamSNRDataList3len)

	for l in range(BestBeamSNRDataList3len):
		plotDistance5[l] = xaxisGraph

	plt.figure(5)
	for index_i in range(len(BestBeamSNRDataList3)):
			if float(BestBeamSNRDataList3[index_i]) < 0:
				plt.scatter(int(plotDistance5[index_i]), float(BestBeamSNRDataList3[index_i]), s = 120, marker="+",color='grey')
			else:
				plt.scatter(int(plotDistance5[index_i]), float(BestBeamSNRDataList3[index_i]), s = 120, marker="+",color='blue')
	plt.scatter(float(xaxisGraph), float(BestBeamSNRDataMostAvgPlot), s= 50, color='red',marker="x")


	BestBeamSNRDataList3 = []



	#Getting Data for LastRemoteRssiData
	LastRemoteRssiData = line.split(',')[3]
	LastRemoteRssiData = LastRemoteRssiData.split()
	lenLastRemoteRssiData = len(LastRemoteRssiData)
	LastRemoteRssiDataMostAvgPlot = line.split(',')[4]
	LastRemoteRssiDataMostAvgPlotlist = LastRemoteRssiDataMostAvgPlotlist + [LastRemoteRssiDataMostAvgPlot]

	# Expand values 
	for element in LastRemoteRssiData:
		LastRemoteRssiDataval = element.split('(')[0]
		LastRemoteRssiDatavalcount = int(element.split('(')[1].split(')')[0])
		for index_i in range(LastRemoteRssiDatavalcount):
			LastRemoteRssiDataList3.append(LastRemoteRssiDataval)

	LastRemoteRssiDataList3len = len(LastRemoteRssiDataList3)


	plotDistance6 = np.zeros(LastRemoteRssiDataList3len)

	for l in range(LastRemoteRssiDataList3len):
		plotDistance6[l] = xaxisGraph

	plt.figure(6)
	for index_i in range(len(LastRemoteRssiDataList3)):
			if float(LastRemoteRssiDataList3[index_i]) < 0:
				plt.scatter(int(plotDistance6[index_i]), float(LastRemoteRssiDataList3[index_i]), s = 120, marker="+",color='grey')
			else:
				plt.scatter(int(plotDistance6[index_i]), float(LastRemoteRssiDataList3[index_i]), s = 120, marker="+",color='blue')
	plt.scatter(float(xaxisGraph), float(LastRemoteRssiDataMostAvgPlot), s= 50, color='red',marker="x")


	LastRemoteRssiDataList3 = []


	#Getting Data for LastBeaconRssiData
	LastBeaconRssiData = line.split(',')[5]
	LastBeaconRssiData = LastBeaconRssiData.split()
	lenLastBeaconRssiData = len(LastBeaconRssiData)
	LastBeaconRssiDataMostAvgPlot = line.split(',')[6]
	LastBeaconRssiDataMostAvgPlotlist = LastBeaconRssiDataMostAvgPlotlist + [LastBeaconRssiDataMostAvgPlot]

	# Expand values 
	for element in LastBeaconRssiData:
		LastBeaconRssiDataval = element.split('(')[0]
		LastBeaconRssiDatavalcount = int(element.split('(')[1].split(')')[0])
		for index_i in range(LastBeaconRssiDatavalcount):
			LastBeaconRssiDataList3.append(LastBeaconRssiDataval)

	LastBeaconRssiDataList3len = len(LastBeaconRssiDataList3)


	plotDistance6 = np.zeros(LastBeaconRssiDataList3len)

	for l in range(LastBeaconRssiDataList3len):
		plotDistance6[l] = xaxisGraph

	plt.figure(7)
	for index_i in range(len(LastBeaconRssiDataList3)):
			if float(LastBeaconRssiDataList3[index_i]) < 0:
				plt.scatter(int(plotDistance6[index_i]), float(LastBeaconRssiDataList3[index_i]), s = 120, marker="+",color='grey')
			else:
				plt.scatter(int(plotDistance6[index_i]), float(LastBeaconRssiDataList3[index_i]), s = 120, marker="+",color='blue')
	plt.scatter(float(xaxisGraph), float(LastBeaconRssiDataMostAvgPlot), s= 50, color='red',marker="x")


	LastBeaconRssiDataList3 = []



	#Getting Data for LastDataRssiData
	LastDataRssiData = line.split(',')[7]
	LastDataRssiData = LastDataRssiData.split()
	lenLastDataRssiData = len(LastDataRssiData)
	LastDataRssiDataMostAvgPlot = line.split(',')[8]
	LastDataRssiDataMostAvgPlotlist = LastDataRssiDataMostAvgPlotlist + [LastDataRssiDataMostAvgPlot]

	# Expand values 
	for element in LastDataRssiData:
		LastDataRssiDataval = element.split('(')[0]
		LastDataRssiDatavalcount = int(element.split('(')[1].split(')')[0])
		for index_i in range(LastDataRssiDatavalcount):
			LastDataRssiDataList3.append(LastDataRssiDataval)

	LastDataRssiDataList3len = len(LastDataRssiDataList3)


	plotDistance6 = np.zeros(LastDataRssiDataList3len)

	for l in range(LastDataRssiDataList3len):
		plotDistance6[l] = xaxisGraph

	plt.figure(8)
	for index_i in range(len(LastDataRssiDataList3)):
			if float(LastDataRssiDataList3[index_i]) < 0:
				plt.scatter(int(plotDistance6[index_i]), float(LastDataRssiDataList3[index_i]), s = 120, marker="+",color='grey')
			else:
				plt.scatter(int(plotDistance6[index_i]), float(LastDataRssiDataList3[index_i]), s = 120, marker="+",color='blue')
	plt.scatter(float(xaxisGraph), float(LastDataRssiDataMostAvgPlot), s= 50, color='red',marker="x")


	LastDataRssiDataList3 = []



	#Getting Data for CurrentMcsData
	CurrentMcsData = line.split(',')[9]
	CurrentMcsData = CurrentMcsData.split()
	lenCurrentMcsData = len(CurrentMcsData)
	CurrentMcsDataMostAvgPlot = line.split(',')[10]
	CurrentMcsDataMostAvgPlotlist = CurrentMcsDataMostAvgPlotlist + [CurrentMcsDataMostAvgPlot]

	# Expand values 
	for element in CurrentMcsData:
		CurrentMcsDataval = element.split('(')[0]
		CurrentMcsDatavalcount = int(element.split('(')[1].split(')')[0])
		for index_i in range(CurrentMcsDatavalcount):
			CurrentMcsDataList3.append(CurrentMcsDataval)

	CurrentMcsDataList3len = len(CurrentMcsDataList3)


	plotDistance6 = np.zeros(CurrentMcsDataList3len)

	for l in range(CurrentMcsDataList3len):
		plotDistance6[l] = xaxisGraph

	plt.figure(9)
	for index_i in range(len(CurrentMcsDataList3)):
			if float(CurrentMcsDataList3[index_i]) < 0:
				plt.scatter(int(plotDistance6[index_i]), float(CurrentMcsDataList3[index_i]), s = 120, marker="+",color='grey')
			else:
				plt.scatter(int(plotDistance6[index_i]), float(CurrentMcsDataList3[index_i]), s = 120, marker="+",color='blue')
	plt.scatter(float(xaxisGraph), float(CurrentMcsDataMostAvgPlot), s= 50, color='red',marker="x")


	CurrentMcsDataList3 = []


	#Getting Data for RFTempData
	RFTempData = line.split(',')[11]
	RFTempData = RFTempData.split()
	lenRFTempData = len(RFTempData)
	RFTempDataMostAvgPlot = line.split(',')[12]
	RFTempDataMostAvgPlotlist = RFTempDataMostAvgPlotlist + [RFTempDataMostAvgPlot]

	# Expand values 
	for element in RFTempData:
		RFTempDataval = element.split('(')[0]
		RFTempDatavalcount = int(element.split('(')[1].split(')')[0])
		for index_i in range(RFTempDatavalcount):
			RFTempDataList3.append(RFTempDataval)

	RFTempDataList3len = len(RFTempDataList3)


	plotDistance6 = np.zeros(RFTempDataList3len)

	for l in range(RFTempDataList3len):
		plotDistance6[l] = xaxisGraph

	plt.figure(10)
	for index_i in range(len(RFTempDataList3)):
			if float(RFTempDataList3[index_i]) < 0:
				plt.scatter(int(plotDistance6[index_i]), float(RFTempDataList3[index_i]), s = 120, marker="+",color='grey')
			else:
				plt.scatter(int(plotDistance6[index_i]), float(RFTempDataList3[index_i]), s = 120, marker="+",color='blue')
	plt.scatter(float(xaxisGraph), float(RFTempDataMostAvgPlot), s= 50, color='red',marker="x")


	RFTempDataList3 = []


	#Getting Data for BBTempData
	BBTempData = line.split(',')[13]
	BBTempData = BBTempData.split()
	lenBBTempData = len(BBTempData)
	BBTempDataMostAvgPlot = line.split(',')[14]
	BBTempDataMostAvgPlotlist = BBTempDataMostAvgPlotlist + [BBTempDataMostAvgPlot]

	# Expand values 
	for element in BBTempData:
		BBTempDataval = element.split('(')[0]
		BBTempDatavalcount = int(element.split('(')[1].split(')')[0])
		for index_i in range(BBTempDatavalcount):
			BBTempDataList3.append(BBTempDataval)

	BBTempDataList3len = len(BBTempDataList3)


	plotDistance6 = np.zeros(BBTempDataList3len)

	for l in range(BBTempDataList3len):
		plotDistance6[l] = xaxisGraph

	plt.figure(11)
	for index_i in range(len(BBTempDataList3)):
			if float(BBTempDataList3[index_i]) < 0:
				plt.scatter(int(plotDistance6[index_i]), float(BBTempDataList3[index_i]), s = 120, marker="+",color='grey')
			else:
				plt.scatter(int(plotDistance6[index_i]), float(BBTempDataList3[index_i]), s = 120, marker="+",color='blue')
	plt.scatter(float(xaxisGraph), float(BBTempDataMostAvgPlot), s= 50, color='red',marker="x")


	BBTempDataList3 = []




############ Zooming in #########################################
	# #Getting Data for SNRData
	# SNRData = line.split(',')[5]
	# SNRData = SNRData.split()
	# lenSNRData = len(SNRData)
	# SNRDataMostAvgPlot = line.split(',')[6]
	# SNRDataMostAvgPlotlist = SNRDataMostAvgPlotlist + [SNRDataMostAvgPlot]

	# # Expand values 
	# for element in SNRData:
	# 	SNRDataval = element.split('(')[0]
	# 	SNRDatavalcount = int(element.split('(')[1].split(')')[0])
	# 	for index_i in range(SNRDatavalcount):
	# 		SNRDataList3.append(SNRDataval)

	# SNRDataList3len = len(SNRDataList3)


	# plotDistance7 = np.zeros(SNRDataList3len)

	# for l in range(SNRDataList3len):
	# 	plotDistance7[l] = xaxisGraph

	# plt.figure(7)

	# plt.subplot(212)
	# plt.axhline(y=0, color='grey',linestyle=':')
	# plt.axhline(y=200, color='yellow',linestyle=':')
	# plt.axhline(y=-10, color='yellow',linestyle=':')

	# linehundred = np.zeros(len(listxaxis2))
	# linenegativeten = np.zeros(len(listxaxis2))
	# for l in range(len(listxaxis2)):
	# 	linehundred[l] = 200
	# 	linenegativeten[l] = -10


	# plt.fill_between(listxaxis2,linehundred,linenegativeten, color='yellow', alpha = 0.2)

	# plt.subplot(211)
	# for index_i in range(len(SNRDataList3)):
	# 		if float(SNRDataList3[index_i]) < 0:
	# 			plt.scatter(plotDistance7[index_i], SNRDataList3[index_i], s = 120, marker="+",color='grey')
	# 		else:
	# 			plt.scatter(plotDistance7[index_i], SNRDataList3[index_i], s = 120, marker="+",color='blue')
	# plt.scatter(xaxisGraph, SNRDataMostAvgPlot, s= 50, color='red',marker="x")


	# plt.subplot(212)
	# for index_i in range(len(SNRDataList3)):
	# 		if float(SNRDataList3[index_i]) < 0:
	# 			plt.scatter(plotDistance7[index_i], SNRDataList3[index_i], s = 120, marker="+",color='grey')
	# 		else:
	# 			plt.scatter(plotDistance7[index_i], SNRDataList3[index_i], s = 120, marker="+",color='blue')
	# plt.scatter(xaxisGraph, SNRDataMostAvgPlot, s= 50, color='red',marker="x")


	# SNRDataList3 = []

#####################################################################################################

inputlogfilename = inputlogfilename[:-4]

listxaxis2 = list(map(float,listxaxis2))
BestBeamSNRDataMostAvgPlotlist = list(map(float,BestBeamSNRDataMostAvgPlotlist))
LastRemoteRssiDataMostAvgPlotlist = list(map(float,LastRemoteRssiDataMostAvgPlotlist))
LastBeaconRssiDataMostAvgPlotlist = list(map(float,LastBeaconRssiDataMostAvgPlotlist))
LastDataRssiDataMostAvgPlotlist = list(map(float,LastDataRssiDataMostAvgPlotlist))
CurrentMcsDataMostAvgPlotlist = list(map(float,CurrentMcsDataMostAvgPlotlist))
RFTempDataMostAvgPlotlist = list(map(float,RFTempDataMostAvgPlotlist))
BBTempDataMostAvgPlotlist = list(map(float,BBTempDataMostAvgPlotlist))


plt.figure(5)
#plt.xticks(arange(len(listxaxis2)),listxaxis2)
#plt.yticks(arange(len(BestBeamSNRDataMostAvgPlotlist)),BestBeamSNRDataMostAvgPlotlist)
plt.gca().set_xlim(left=0)
plt.xlabel('Distance')
plt.ylabel('BestBeamSNRData')
plt.title('Distance(m) v BestBeamSNRData',fontweight="bold")
plt.axhline(y=0, color='grey',linestyle=':')
#plt.axhline(y=1000, color='green',linestyle=':')
plt.plot(listxaxis2,BestBeamSNRDataMostAvgPlotlist, "-", color = "red")
red_line = mlines.Line2D( [],[], color='red' , marker='x', markersize=10, label='Average BestBeamSNRData')
Blue_cross = mlines.Line2D( [],[], color='b' , marker='+', markersize=10, label='BestBeamSNRData', linewidth = 0)
lgd = plt.legend(handles=[red_line,Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_dist_vs_BestBeamSNR_data"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_stat_bestbeamsnr_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')


plt.figure(6)
plt.gca().set_xlim(left=0)
plt.xlabel('Distance')
plt.ylabel('LastRemoteRssiData')
plt.title('Distance(m) v LastRemoteRssiData',fontweight="bold")
plt.axhline(y=0, color='grey',linestyle=':')
#plt.axhline(y=1000, color='green',linestyle=':')
plt.plot(listxaxis2, LastRemoteRssiDataMostAvgPlotlist, "-", color = "red")
red_line = mlines.Line2D( [], [], color='red' , marker='x', markersize=10, label='Average LastRemoteRssiData')
Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='LastRemoteRssiData', linewidth = 0)
lgd = plt.legend(handles=[red_line,Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_dist_vs_LastRemoteRssi_data"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_stat_lastremoterssi_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')


plt.figure(7)
plt.gca().set_xlim(left=0)
plt.xlabel('Distance')
plt.ylabel('LastBeaconRssiData')
plt.title('Distance(m) v LastBeaconRssiData',fontweight="bold")
plt.axhline(y=0, color='grey',linestyle=':')
#plt.axhline(y=1000, color='green',linestyle=':')
plt.plot(listxaxis2, LastBeaconRssiDataMostAvgPlotlist, "-", color = "red")
red_line = mlines.Line2D( [], [], color='red' , marker='x', markersize=10, label='Average LastBeaconRssiData')
Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='LastBeaconRssiData', linewidth = 0)
lgd = plt.legend(handles=[red_line,Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_dist_vs_LastBeaconRssi_data"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_stat_lastbeaconrssi_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')


plt.figure(8)
plt.gca().set_xlim(left=0)
plt.xlabel('Distance')
plt.ylabel('LastDataRssiData')
plt.title('Distance(m) v LastDataRssiData',fontweight="bold")
plt.axhline(y=0, color='grey',linestyle=':')
#plt.axhline(y=1000, color='green',linestyle=':')
plt.plot(listxaxis2, LastDataRssiDataMostAvgPlotlist, "-", color = "red")
red_line = mlines.Line2D( [], [], color='red' , marker='x', markersize=10, label='Average LastDataRssiData')
Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='LastDataRssiData', linewidth = 0)
lgd = plt.legend(handles=[red_line,Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_dist_vs_LastDataRssi_data"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_stat_lastdatarssi_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')


plt.figure(9)
plt.gca().set_xlim(left=0)
plt.xlabel('Distance')
plt.ylabel('CurrentMcsData')
plt.title('Distance(m) v CurrentMcsData',fontweight="bold")
plt.axhline(y=0, color='grey',linestyle=':')
#plt.axhline(y=1000, color='green',linestyle=':')
plt.plot(listxaxis2, CurrentMcsDataMostAvgPlotlist, "-", color = "red")
red_line = mlines.Line2D( [], [], color='red' , marker='x', markersize=10, label='Most Frequent CurrentMcsData')
Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='CurrentMcsData', linewidth = 0)
lgd = plt.legend(handles=[red_line,Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_dist_vs_CurrentMcs_data"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_stat_currentmcs_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

plt.figure(10)
plt.gca().set_xlim(left=0)
plt.xlabel('Distance')
plt.ylabel('RFTempData')
plt.title('Distance(m) v RFTempData',fontweight="bold")
plt.axhline(y=0, color='grey',linestyle=':')
#plt.axhline(y=1000, color='green',linestyle=':')
plt.plot(listxaxis2, RFTempDataMostAvgPlotlist, "-", color = "red")
red_line = mlines.Line2D( [], [], color='red' , marker='x', markersize=10, label='Average RFTempData')
Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='RFTempData', linewidth = 0)
lgd = plt.legend(handles=[red_line,Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_dist_vs_RFTemp_data"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_stat_rftemp_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')




plt.figure(11)
plt.gca().set_xlim(left=0)
plt.xlabel('Distance')
plt.ylabel('BBTempData')
plt.title('Distance(m) v BBTempData' , fontweight="bold")
plt.axhline(y=0, color='grey',linestyle=':')
#plt.axhline(y=1000, color='green',linestyle=':')

plt.plot(listxaxis2, BBTempDataMostAvgPlotlist, "-", color = "red")
red_line = mlines.Line2D( [], [], color='red' , marker='x', markersize=10, label='Average BBTempData')
Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='BBTempData', linewidth = 0)
lgd = plt.legend(handles=[red_line,Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_dist_vs_bbtemp_data_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_stat_bbtemp_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

################# Zooming in graph plot code ########################################

# #
# plt.figure(9)
# plt.gca().set_xlim(left=0)
# plt.xlabel('Distance')
# plt.ylabel('RSSIData')
# plt.title('Distance(m) v RSSIData')
# plt.axhline(y=0, color='grey',linestyle=':')
# #plt.axhline(y=1000, color='green',linestyle=':')
# plt.plot(listxaxis2, RSSIDataMostAvgPlotlist, "-", color = "red")
# red_line = mlines.Line2D( [], [], color='red' , marker='x', markersize=10, label='Most Frequent RSSIData')
# Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='RSSIData', linewidth = 0)
# lgd = plt.legend(handles=[red_line,Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
# plt.savefig(inputlogfiledir+OUTPUT_FOLDER+"graph_dist_vs_RSSI_data"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')



# #Adjusting SNRData plots (Part 1)

# plt.figure(7)
# plt.subplot(211)
# plt.axhline(y=0, color='grey',linestyle=':')
# plt.axhline(y=200, color='yellow',linestyle=':')
# plt.axhline(y=-10, color='yellow',linestyle=':')

# linehundred = np.zeros(len(listxaxis2))
# linenegativeten = np.zeros(len(listxaxis2))
# for l in range(len(listxaxis2)):
# 	linehundred[l] = 200
# 	linenegativeten[l] = -10


# plt.fill_between(listxaxis2,linehundred,linenegativeten, color='yellow')




# # #Adjusting SNRData plots (Part 1)

# plt.figure(7)
# plt.subplot(211)

# linehundred = np.zeros(len(listxaxis2))
# linenegativeten = np.zeros(len(listxaxis2))
# for l in range(len(listxaxis2)):
# 	linehundred[l] = 200
# 	linenegativeten[l] = -10

# plt.gca().set_xlim(left=0)
# plt.ylabel('SNRData')
# plt.title('Distance(m) v SNRData (Full)')
# plt.axhline(y=0, color='grey',linestyle=':')


# #plt.axhline(y=1000, color='green',linestyle=':')

# plt.plot(listxaxis2, SNRDataMostAvgPlotlist, "-", color = "red")
# red_line = mlines.Line2D( [], [], color='red' , marker='x', markersize=10, label='Most Frequent SNRData')
# Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='SNRData', linewidth = 0)
# lgd = plt.legend(handles=[red_line,Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-1.5))


# plt.subplot(212)
# plt.axhline(y=0, color='grey',linestyle=':')
# plt.axhline(y=100, color='yellow',linestyle=':')
# plt.axhline(y=-10, color='yellow',linestyle=':')
# plt.xlabel('Distance')

# linehundred = np.zeros(len(listxaxis2))
# linenegativeten = np.zeros(len(listxaxis2))
# for l in range(len(listxaxis2)):
# 	linehundred[l] = 200
# 	linenegativeten[l] = -10


# plt.fill_between(listxaxis2,linehundred,linenegativeten, color='yellow', alpha = 0.1)

# plt.title('Distance(m) v SNRData (Zoomed)')
# plt.ylim(-10, 200)
# plt.ylabel('SNRData')

# plt.gca().set_xlim(left=0)
# plt.plot(listxaxis2, SNRDataMostAvgPlotlist, "-", color = "red")
# plt.savefig(inputlogfiledir+OUTPUT_FOLDER+"graph_dist_vs_SNR_data"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

#####################################################################################################




listxaxis2 = []

# Remove temp files
try:
	os.remove(outputextractstatsup)
except:
	donothing=1	
try:
	os.remove(outputextractstatsupsorted)
except:
	donothing=1	
			

