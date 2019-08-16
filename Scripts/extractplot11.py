import sys, math
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
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
udpAvgDataPlotLIST = []
tcpAvgDataPlotLIST = []
pingAvgDataPlotLIST = []
listxaxis2 = []
startOffFrom = 2 # second
TimeStampConnectedStart = []
TimeStampDisconnectedEnd = []
lineconnectedtrue= 0
collectperiodsec= 5
TxSectorDataList = []
RxSectorDataList = []
SNRDataList = []
RemoteSNRDataList = []
RSSIDataList = []
OUTPUT_FOLDER = "Results/"
OUTPUT_FOLDER2 = "Results/Graphs/"
OUTPUT_FOLDER3 = "Results/Consolidated files/"
TIMESTAMPLENGTH = 17 # hardcoded!
SKIPFIRSTREADING = 1 # set to 1 to ignore first measurement (note: sometimes first readings are significantly worse)
timestamplist = []

#Finding total SNR, RemoteSNR and RSSI 
TotalSNR = 0.0
TotalRemoteSNR = 0.0 
TotalRSSI = 0.0

TotalSNR2 = 0.0
TotalRemoteSNR2 = 0.0 
TotalRSSI2 = 0.0


## main
print "INFO: START EXTRACT PLOT\n"

# Get log file name and check if valid
if len(sys.argv) != 2:
	print "Correct usage: python extractplot<ver>.py [dir]/[filename].csv"
	quit() # not valid so exit

if SKIPFIRSTREADING  == 1:
	print "Note: Skip first reading: Enabled (to avoid abnormal values)"

inputlogfile = sys.argv[1]
# inputlogfiledir = os.path.dirname(os.path.realpath(inputlogfile)) + "/"
inputlogfiledir = str(inputlogfile.rsplit('/',1)[0]) + "/"
inputlogfilename = os.path.basename(inputlogfile)

outputextractsup = inputlogfiledir+OUTPUT_FOLDER+"output_sup_"+inputlogfilename
outputextractsupsorted = inputlogfiledir+OUTPUT_FOLDER+"output_sorted_sup_"+inputlogfilename
outputextractsupsortedmerged = inputlogfiledir+OUTPUT_FOLDER3+"output_sortedmerged_sup_"+inputlogfilename
outputextractperf = inputlogfiledir+OUTPUT_FOLDER+"output_perf_"+inputlogfilename
outputextractperfsorted = inputlogfiledir+OUTPUT_FOLDER+"output_sorted_perf_"+inputlogfilename
outputextractperfsortedmerged = inputlogfiledir+OUTPUT_FOLDER3+"output_sortedmerged_perf_"+inputlogfilename
outputextractsupperfsortedmerged = inputlogfiledir+OUTPUT_FOLDER+"output_sortedmerged_supperf_"+inputlogfilename

#Creates empty files
supfile = open(outputextractsup, "w")
supfile.close()
supsortedfile = open(outputextractsupsorted, "w")
supsortedfile.close()
supsortedmergedfile = open(outputextractsupsortedmerged, "w")
supsortedmergedfile.close()
perffile = open(outputextractperf, "w")
perffile.close()
perfsortedfile = open(outputextractperfsorted, "w")
perfsortedfile.close()
perfsortedmergedfile = open(outputextractperfsortedmerged, "w")
perfsortedmergedfile.close()
supperfsortedmergedfile = open(outputextractsupperfsortedmerged, "w")
supperfsortedmergedfile.close()

print "\nSummary:"
print "Input:"
print inputlogfile
print "Output:"
#print outputextractsup
# print outputextractsupsorted
print outputextractsupsortedmerged
# print outputextractperf
# print outputextractperfsorted
print outputextractperfsortedmerged
print outputextractsupperfsortedmerged

#Creating headers
with open(outputextractsup, "wb") as supfile:
	writer4 = csv.DictWriter(supfile, fieldnames = ["Distance", "TxSectorData", "Frequent TxSectorData", "RxSectorData", "Frequent RxSectorData",  "SNRData", "Average SNRData Div 8" , "RemoteSNRData" , "Average RemoteSNRData Div 8" , "RSSIData" , "Average RSSIData"], delimiter = ',' )
	writer4.writeheader()
supfile.close()

with open(outputextractsupsortedmerged, "wb") as supsortedmergedfile:
	writer4 = csv.DictWriter(supsortedmergedfile, fieldnames = ["Distance", "TxSectorData", "Frequent TxSectorData", "RxSectorData", "Frequent RxSectorData",  "SNRData", "Average SNRData Div 8" , "RemoteSNRData" , "Average RemoteSNRData Div 8" , "RSSIData" , "Average RSSIData"], delimiter = ',' )
	writer4.writeheader()
supsortedmergedfile.close()

with open(outputextractperfsortedmerged, "wb") as perfsortedmergedfile:
	writer2 = csv.DictWriter(perfsortedmergedfile, fieldnames = ["Distance", "Ping Values", "Avg Ping Values", "Udp Values",  "Avg Udp Values", "Tcp Values" , "Avg Tcp Values"], delimiter = ',' )
	writer2.writeheader()
perfsortedmergedfile.close()

#Assigns header to each file
with open(outputextractperf, "a") as perffile: #Change file name here
	writer = csv.DictWriter(perffile, fieldnames = ["Distance", "Ping Values", "Avg Ping Values", "Udp Values",  "Avg Udp Values", "Tcp Values" , "Avg Tcp Values"], delimiter = ',' )
	writer.writeheader()
perffile.close()

with open(outputextractsupperfsortedmerged, "wb") as supperfsortedmergedfile:
	writer5 = csv.DictWriter(supperfsortedmergedfile, fieldnames = ["Distance","Frequent TxSectorData","Frequent RxSectorData","Average SNRData Div 8" ,"Average RemoteSNRData Div 8" ,"Average RSSIData","Avg Ping Values","Avg Udp Values","Avg Tcp Values"], delimiter = ',' )
	writer5.writeheader()
supperfsortedmergedfile.close()



#Code: plots latest data collected from each file
with open(inputlogfile, "rt") as inputlog: #Input main file name
	inputlogcontent = inputlog.readlines()[1:]
	for line in inputlogcontent:
		listUdpValue = []
		listTcpValue = []
		xaxis = float(line.split(",")[2]) #find x axis
		udpFilePathName = inputlogfiledir + str(line.split(",")[11]) #find udp files
		#print udpFilePathName
		pingFilePathName = inputlogfiledir + str(line.split(",")[10]) #finds ping file
		#print pingFilePathName
		tcpFilePathName = inputlogfiledir + str(line.split(",")[12]) #find tcp files
		#print tcpFilePathName
		supFilePathName = inputlogfiledir + str(line.split(",")[8]) #find sup files
		#print supFilePathName
		#tcpFilePathName = tcpFilePathName.rstrip() (Needed for if tcp file is last col in csv file)

		# print udpFilePathName
		# print pingFilePathName
		# print tcpFilePathName
		# print supFilePathName

		print "INFO: PROCESSING TCP FILE\n"

		# Allows break to exit
		for index_i in range(1):
	#Opening each tcp files
			if len(tcpFilePathName) > (1+len(inputlogfiledir)):
				try:
					with open(tcpFilePathName, "rt") as tcpFile:
							tcpFile = tcpFile.readlines()
							
							# check if file is empty
							if len(tcpFile) < 2:	# i.e. empty file (only initial timestamp text)
								print "WARNING ("+tcpFilePathName+": empty)"
								listTcpValue = []
								listTcpValue = [-1]
								valueAvgTcp = -1
								break

							tcpFile = np.array(tcpFile)
		#Finds the last row 
							myrowtcp = tcpFile.shape 
							myrowtcp = int(myrowtcp[0])
		#Reads the data in reverse : lastest data is now read from top
							tcpFile = tcpFile[myrowtcp::-1]
		#Count each row and retreive latest data by finding ("-------------")
							for i, line in enumerate(tcpFile):
								if myKeyWord in line:
									tcpFile = tcpFile[0:i]
		#Flips data read again
							tcpFile = tcpFile[::-1] 

		#Extracting data using key word "bits/sec"
					skippedfirstreading = 0
					for line in tcpFile:
						for phrase in keep_phrases:
							if phrase in line: 
		#Makes a list called "importanttcp"
								importanttcp.append(line) 
								break
			
		#Finding and sorting of avg bandwidth and yaxis (newBytes) data
					for line in importanttcp:
						if SortingKeyWord in line: #Converting to Mbits/sec from Gbits/sec
							# check if need to skip first reading
							if SKIPFIRSTREADING == 1 and skippedfirstreading == 0:
								skippedfirstreading = 1
							else:
								splitlinetcp = line.split()
								splitlen=len(splitlinetcp)
			#Counts cols in reverse
								numbertcp = float(line.split()[(splitlen-2)])
								numbertcp = numbertcp * 1000
			#Every data put into list: listTcpValue
								listTcpValue += [numbertcp]
								valueAvgTcp += numbertcp
						if SortingKeyWord2 in line: 
							if SKIPFIRSTREADING == 1 and skippedfirstreading == 0:
								skippedfirstreading = 1
							else:					
								splitlinetcp = line.split()
								splitlen=len(splitlinetcp)
								numbertcp = float(line.split()[(splitlen-2)])
								listTcpValue += [numbertcp]
								valueAvgTcp += numbertcp
						if SortingKeyWord3 in line: #Converting to Mbits/sec from Gbits.sec
							if SKIPFIRSTREADING == 1 and skippedfirstreading == 0:
								skippedfirstreading = 1
							else:					
								splitlinetcp = line.split()
								splitlen=len(splitlinetcp)
								numbertcp = float(line.split()[(splitlen-2)])
								numbertcp = numbertcp * 125
								listTcpValue += [numbertcp]
								valueAvgTcp += numbertcp

		#Resets main list of strings 
						importanttcp = []

					if len(listTcpValue) == 0:
						print "WARNING ("+tcpFilePathName +": no values)"				
						listTcpValue = []
						listTcpValue = [-1]
						valueAvgTcp = -1
						break
					valueAvgTcp = valueAvgTcp/len(listTcpValue)

				except IOError:
					print "WARNING (IOERROR: " + tcpFilePathName +" Tcp file not found)"
					listTcpValue = []
					listTcpValue = [-1]
					valueAvgTcp = -1

			else:
				listTcpValue = [-1]
				valueAvgTcp = -1

		print "INFO: PROCESSING PING FILE\n"

		# Allows break to exit	
		for index_i in range(1):
	#Skips if file is empty
	#Finds pingAvg value 
			if len(pingFilePathName) > (1+len(inputlogfiledir)):
				try:
					with open(pingFilePathName, "rt") as pingFile:
							pingFile = pingFile.readlines()

							# Check if file is empty
							if len(pingFile) < 2:	# i.e. empty file (only initial timestamp text)
								print "WARNING ("+pingFilePathName+": empty)"
								listPingValue = []
								listPingValue = [-1]
								valueAvgPing = -1
								break
		#resets list of ping values
							listPingValue = []
							skippedfirstreading = 0
							for line in pingFile:
		#Find the start value for SUP file
								if startSupKeyWord in line:
									startSup = line.split(' ')[0]
		#Find ping values & avg  ping value						
								if pingTime in line:
									if SKIPFIRSTREADING == 1 and skippedfirstreading == 0:
										skippedfirstreading = 1
									else:								
										timePing = line.split('=')[3]
										pingValue = timePing.split()[-2]
										endSup = line.split(" ")[0] #Finds the end value for SupFile
										listPingValue += [pingValue]
										pingValue = float(pingValue)
										avgPing += pingValue
							valueAvgPing = avgPing / len(listPingValue)
				except IOError:
					print "WARNING (IOERROR: " + pingFilePathName +" Ping file not found)"
					listPingValue = []
					listPingValue = [-1]
					valueAvgPing = -1
							
			else:
				listPingValue = [-1]
				valueAvgPing = -1

# 		print startSup
# 		print endSup

		print "INFO: PROCESSING UDP FILE\n"

		# Allows break to exit
		for index_i in range(1):

			#Skips line udp file if '-'
			if len(udpFilePathName) > (1+len(inputlogfiledir)):
				valueAvgUdp = 1
				try:
	#Opening each udp files
					with open(udpFilePathName, "rt") as udpFile: 
						udpFile = udpFile.readlines()


						# Check if file is empty
						if len(udpFile) < 2:	# i.e. empty file (only initial timestamp text)
							print "WARNING ("+udpFilePathName+": empty)"
							listUdpValue = []
							listUdpValue = [-1]
							valueAvgUdp = -1
							break

						udpFile = np.array(udpFile)
	#Finds the last row 
						myrowudp = udpFile.shape 
						myrowudp = int(myrowudp[0])
	#Reads the data in reverse : lastest data is now read from top
						udpFile = udpFile[myrowudp::-1]
	#Count each row and retreive latest data by finding ("-------------")
						for i, line in enumerate(udpFile):
							if myKeyWord in line:
								udpFile = udpFile[0:i]
	#Flips data read again
						udpFile = udpFile[::-1] 	
		#Extracting data using key word "bits/sec"
					for line in udpFile:
						for phrase in keep_phrases:
							if phrase in line: 
		#Makes a list called "importantudp"
								importantudp.append(line) 
								break

		#Finding and sorting of avg bandwidth and yaxis (newBytes) data
					skippedfirstreading = 0
					for line in importantudp:
		#Sorting line by Gbit/sec
						if SortingKeyWord in line:
							if SKIPFIRSTREADING == 1 and skippedfirstreading == 0:
								skippedfirstreading = 1
							else:						
								splitlineudp = line.partition("Gbits/sec")[0]
								splitlineudp = splitlineudp.split()
								numberudp = float(splitlineudp[-1])
								numberudp = numberudp * 1000
								#jitter = float(line.split()[splitlen-5])
								#datagrams = str(line.split()[splitlen-1]) 
			#Every data put into list: listUdpValue
								listUdpValue += [numberudp]
								valueAvgUdp += numberudp
		#Sorting line by Mbits/sec		
						if SortingKeyWord2 in line:
							if SKIPFIRSTREADING == 1 and skippedfirstreading == 0:
								skippedfirstreading = 1
							else:
								splitlineudp = line.partition("Mbits/sec")[0]
								splitlineudp = splitlineudp.split()
								numberudp = float(splitlineudp[-1])
								listUdpValue += [numberudp]
								valueAvgUdp += numberudp

						if SortingKeyWord3 in line:
							if SKIPFIRSTREADING == 1 and skippedfirstreading == 0:
								skippedfirstreading = 1
							else:
								splitlineudp = line.partition("Kbits/sec")[0]
								splitlineudp = splitlineudp.split()
								numberudp = float(splitlineudp[-1])
								numberudp = numberudp *125
								listUdpValue += [numberudp]
								valueAvgUdp += numberudp

		#Resets main list of strings 
						importantudp = []
					valueAvgUdp = valueAvgUdp
					x = len(listUdpValue)
					if len(listUdpValue) == 0:
						print "WARNING ("+udpFilePathName +": no values)"				
						listUdpValue = []
						listUdpValue = [-1]
						valueAvgUdp = -1
						break
					valueAvgUdp = valueAvgUdp/len(listUdpValue)
				except IOError:
					print "WARNING (IOERROR: " + udpFilePathName +" Udp file not found)"
					listUdpValue = []
					listUdpValue = [-1]
					valueAvgUdp = -1

			else:
				listUdpValue = [-1]
				valueAvgUdp = -1		


		print "INFO: WRITING PERF TO CSV\n"

#Write to CSV file: "Distance", "Ping Values", "Avg Ping Values", "Udp Values",  "Avg Udp Values", "Tcp Values" , "Avg Tcp Values
		csvline = str(xaxis) + ","
		for j in range(len(listPingValue)):
			csvline += str(listPingValue[j])
			if j < len(listPingValue)-1:
				csvline += " "
		csvline += "," + str(valueAvgPing) + ","
		for i in range(len(listUdpValue)):
			csvline += str(listUdpValue[i])
			if i < len(listUdpValue)-1:
				csvline += " "
		csvline += "," + str(valueAvgUdp) + ","
		for k in range(len(listTcpValue)):
			csvline += str(listTcpValue[k])
			if k < len(listTcpValue)-1:
				csvline += " "
		csvline += "," + str(valueAvgTcp)
			
#Print csvline in file "DIstance_Vs_ Bandwidth.csv
		with open(outputextractperf, "a") as perffile: #Change file name here
			perffile.write(csvline + "\n")
		perffile.close()

#Creates array for xaxis
		plotDistance = np.zeros(len(listUdpValue))
		plotDistance2 = np.zeros(len(listTcpValue))
		
	
#Fills array with xaxis
		for i in range(len(listUdpValue)):
			plotDistance[i] = xaxis	
		for j in range(len(listTcpValue)):
			plotDistance2[j] = xaxis	
		
#Plots data: Adjust settings here
		plt.figure(1)		
		plt.scatter(plotDistance, listUdpValue, s = 120, marker="+")
		plt.scatter(xaxis, valueAvgUdp, s= 50, color='red',marker="x")

		plt.figure(2)
		plt.scatter(plotDistance2, listTcpValue, s = 120, marker="+")
		plt.scatter(xaxis, valueAvgTcp, s=50, color='red',marker="x")
#Resets average numbers for tcp , udp and ping
		valueAvgUdp = 0
		valueAvgTcp = 0 
		avgPing = 0


		print "INFO: PROCESSING SUP FILE\n"

		#Opening each Sup File
		# with open(supFilePathName, "rt") as SupFile:
		# 	SupFile = SupFile.readlines()[1:]
		# 	for line in SupFile:
		# 		supFileValue = line.split(' ')[0]
		# 		if supFileValue >= startSup and supFileValue <= endSup:
		# 			#print supFileValue
		# 			print line  

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

		#to check
		#print udpFilePathName
		#print tcpFilePathName
		#print timestamplist
		#print earliesttimestamp
		#print latesttimestamp

		#clear timestamplist to prevent repeat
		timestamplist = []

############################################################################



		# Note: assumed that sup file always exists and not empty
		with open(supFilePathName, "rt") as SupFile:
			#print supFilePathName
			SupFilelines = SupFile.readlines()

			# lineconnectedtrue= 0
			for line in SupFilelines:
				#print  line
				TimestampLine = line.split(" ")[0]
				if len(TimestampLine) != TIMESTAMPLENGTH:
					donothing = 1
					#print "WARNING ("+supFilePathName+" has line without timestamp)"
					continue
				
				if float(TimestampLine) >= float(earliesttimestamp) and float(TimestampLine) <= float(latesttimestamp): 
					for phrases in BFevent_data:
						if phrases in line:
							dataList = line.split(" ")[2]
							TxSectorData = dataList.split(',')[0]
							TxSectorDataList = TxSectorDataList + [TxSectorData]
							RxSectorData = dataList.split(',')[1]
							RxSectorDataList = RxSectorDataList + [RxSectorData]
							
							SNRData = dataList.split(',')[2]
							TotalSNR = TotalSNR + float(SNRData)
							SNRDataList = SNRDataList + [SNRData]
							

							RemoteSNRData = dataList.split(',')[3]
							TotalRemoteSNR = TotalRemoteSNR + float(RemoteSNRData)
							RemoteSNRDataList = RemoteSNRDataList + [RemoteSNRData]


							RSSIData = dataList.split(',')[4]
							TotalRSSI = TotalRSSI + float(RSSIData)
							RSSIDataList = RSSIDataList + [RSSIData]

				# elif float(TimestampLine) > (float(TimeStampConnectedStart) + collectperiodsec): #Case to stop printing
				# 	lineconnectedtrue=2 #set to 2 to prevent repeating timestampconnected update and printing 


# get counts for each unique value
			if (len(TxSectorDataList)>0):

				a = TxSectorDataList
				#print a 
				aCount = {x:a.count(x) for x in a}
				#valuesA = sorted(aCount.values())
				countA = sorted(aCount, key=aCount.get)
				#print countA
				mostFrequentTxSectorData = countA[-1]

	# sort list in ascending order
				TxSectorDataCountSorted = sorted(aCount.items(), key = lambda x:int(x[0]))

	#formats everthing
				TxSectorDataCountFormatted = str(TxSectorDataCountSorted).strip('[]')
				TxSectorDataCountFormatted = TxSectorDataCountFormatted.replace("('","")
				TxSectorDataCountFormatted = TxSectorDataCountFormatted.replace("', ","(")
				TxSectorDataCountFormatted = TxSectorDataCountFormatted.replace(",","")
			else:
				TxSectorDataCountFormatted=""

#Steps repeated for rest of RxSector, SNR, RemoteSNR, RRSI
			if (len(RxSectorDataList)>0):

				b = RxSectorDataList
				bCount = {xx:b.count(xx) for xx in b}
				countB = sorted(bCount, key=bCount.get)
				mostFrequentRxSectorData = countB[-1]

				RxSectorDataCountSorted = sorted(bCount.items(), key = lambda x:int(x[0]))

				RxSectorDataCountFormatted = str(RxSectorDataCountSorted).strip('[]')
				RxSectorDataCountFormatted = RxSectorDataCountFormatted.replace("('","")
				RxSectorDataCountFormatted = RxSectorDataCountFormatted.replace("', ","(")
				RxSectorDataCountFormatted = RxSectorDataCountFormatted.replace(",","")
			else:
				RxSectorDataCountFormatted=""

			if (len(SNRDataList)>0):

				c = SNRDataList
				cCount = {xxx:c.count(xxx) for xxx in c}
				countC = sorted(cCount, key=cCount.get)
				mostFrequentSNRData = countC[-1]

				SNRDataListLength = len(SNRDataList)
				AverageSNRData = TotalSNR / SNRDataListLength
				AverageSNRData = AverageSNRData / 8                             #Average SNR data is divided by 8 on purpose


				SNRDataDataCountSorted = sorted(cCount.items(), key = lambda x:int(x[0]))

				SNRDataDataCountFormatted = str(SNRDataDataCountSorted).strip('[]')
				SNRDataDataCountFormatted = SNRDataDataCountFormatted.replace("('","")
				SNRDataDataCountFormatted = SNRDataDataCountFormatted.replace("', ","(")
				SNRDataDataCountFormatted = SNRDataDataCountFormatted.replace(",","")
			else:
				SNRDataDataCountFormatted=""

			if (len(RemoteSNRDataList)>0):

				d = RemoteSNRDataList
				dCount = {xxxx:d.count(xxxx) for xxxx in d}
				countD = sorted(dCount, key=dCount.get)
				mostFrequentRemoteSNRData = countD[-1]

				RemoteSNRDataListLength = len(RemoteSNRDataList)
				AverageRemoteSNRData = TotalRemoteSNR / RemoteSNRDataListLength
				AverageRemoteSNRData = AverageRemoteSNRData / 8                   #Average RemoteSNR data is divided by 8 on purpose


				RemoteSNRDataCountSorted = sorted(dCount.items(), key = lambda x:int(x[0]))

				RemoteSNRDataCountFormatted = str(RemoteSNRDataCountSorted).strip('[]')
				RemoteSNRDataCountFormatted = RemoteSNRDataCountFormatted.replace("('","")
				RemoteSNRDataCountFormatted = RemoteSNRDataCountFormatted.replace("', ","(")
				RemoteSNRDataCountFormatted = RemoteSNRDataCountFormatted.replace(",","")
			else:
				RemoteSNRDataCountFormatted=""

			if (len(RSSIDataList)>0):

				e = RSSIDataList
				eCount = {xxxxx:e.count(xxxxx) for xxxxx in e}
				countE = sorted(eCount, key=eCount.get)
				mostFrequentRSSIData = countE[-1]

				RSSIDataListLength = len(RSSIDataList)
				AverageRSSIData = TotalRSSI / RSSIDataListLength

				RSSIDataCountSorted = sorted(eCount.items(), key = lambda x:int(x[0]))

				RSSIDataCountFormatted = str(RSSIDataCountSorted).strip('[]')
				RSSIDataCountFormatted = RSSIDataCountFormatted.replace("('","")
				RSSIDataCountFormatted = RSSIDataCountFormatted.replace("', ","(")
				RSSIDataCountFormatted = RSSIDataCountFormatted.replace(",","")
			else:
				RSSIDataCountFormatted=""

			TxSectorDataList = []
			RxSectorDataList = []
			SNRDataList = []
			RemoteSNRDataList = []
			RSSIDataList = []

			TotalRSSI = 0.0
			TotalSNR = 0.0
			TotalRemoteSNR = 0.0

			#Creates CSV file

			with open(outputextractsup, "a") as supfile: #Change file name here
				supfile.write(str(xaxis) +","+ TxSectorDataCountFormatted + "," + mostFrequentTxSectorData + "," + RxSectorDataCountFormatted + "," + mostFrequentRxSectorData + "," + SNRDataDataCountFormatted + "," + str(AverageSNRData) + "," + RemoteSNRDataCountFormatted + "," + str(AverageRemoteSNRData) + "," + RSSIDataCountFormatted + "," + str(AverageRSSIData) + "\n")
			supfile.close()		

N=50
colors = np.random.rand(N)

#Set graph
plt.figure(1)
plt.gca().set_xlim(left=0)
plt.xlabel('Distance')
plt.ylabel('Udp_Bandwidth')
plt.title('Distance v Udp_Bandwidth (Not Merged)',fontweight="bold")
plt.axhline(y=0, color='grey',linestyle=':')
plt.axhline(y=1000, color='green',linestyle=':')
red_line = mlines.Line2D( [], [], color='red' , marker='x', markersize=10, label='Avg Bandwidth')
Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='Bandwidth', linewidth = 0)
lgd = plt.legend(handles=[red_line,Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_dist_vs_udp_"+inputlogfilename+" (not merged).png")

plt.figure(2)
plt.gca().set_xlim(left=0)
plt.xlabel('Distance')
plt.ylabel('Tcp_Bandwidth')
plt.title('Distance v Tcp_Bandwidth (Not Merged)',fontweight="bold")
plt.axhline(y=0, color='grey',linestyle=':')
plt.axhline(y=1000, color='green',linestyle=':')
red_line = mlines.Line2D( [], [], color='red' , marker='x', markersize=10, label='Avg Bandwidth')
Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='Bandwidth', linewidth = 0)
lgd = plt.legend(handles=[red_line,Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_dist_vs_tcp_"+inputlogfilename+" (not merged).png")


#if want to see graph
#plt.show()



#Merge data (perf) based on distacce (every distance only have 1 row) - save as different file ; orig, sorted, merge sorted file 

print "INFO: SORT AND MERGE PERF\n"

#Opens output file and sorts according to distance
with open(outputextractperf , 'r') as data:
	data = csv.reader(data,delimiter=',')
	data.next()
	list1 = sorted(data, key=lambda x: (float(x[0])))

#Creates new file "output_sorted"
with open(outputextractperfsorted, "wb") as f:
	fileWriter = csv.writer(f, delimiter=',')
	writer = csv.DictWriter(f, fieldnames = ["Distance", "Ping Values", "Avg Ping Values", "Udp Values",  "Avg Udp Values", "Tcp Values" , "Avg Tcp Values"], delimiter = ',' )
	writer.writeheader()
	for row in list1:
		fileWriter.writerow(row)
f.close()

#Start merging same distances (perf)

with open(outputextractperfsorted, "r") as merge1perf:
	merge1linesperf = merge1perf.readlines()[1:]
	merge2linesperf = merge1linesperf

merge1Index = -1
merge1NextIndex = 1

for line in merge1linesperf:
	merge1Index = merge1Index+1
	combineFlag = 0
	if merge1Index == 0 or merge1Index == merge1NextIndex:
		merge2Index = -1		
		merge1col = line.split(',')[0]
		for line2 in merge2linesperf:
			merge2Index = merge2Index + 1
			merge2col = line2.split(',')[0]			
			if merge2Index > merge1Index: #starting one more than previous 

#Data is matched and merged if equal
				if merge1col == merge2col:
					combineFlag = 1
#Find new average for Ping Data
					pingData = line.split(',')[1] + " " + line2.split(',')[1]
					pingData = pingData.split()
					lenPingData = len(pingData)
					for element in pingData:
						element = float(element)
						if element == -1:
							lenPingData = lenPingData - 1
						if element > 0: 
							sumData1 = sumData1 + element
					mergedPingAveData = sumData1 / lenPingData
					sumData1 = 0 
#Find new average for Udp Data
					udpData = line.split(',')[3] + " " + line2.split(',')[3]
					udpData = udpData.split()
					lenUdpData = len(udpData)
					for element in udpData:
						element = float(element)
						if element == -1:
							lenUdpData  = lenUdpData  - 1
						if element > 0: 
							sumData2 = sumData2 + element
					mergedUdpAveData = sumData2 / lenUdpData 
					sumData2 = 0
#Find new average for Tcp Data
					tcpData = line.split(',')[5] + " " + line2.split(',')[5]
					tcpData = tcpData.split()
					lenTcpData = len(tcpData)
					for element in tcpData:
						element = float(element)
						if element == -1:
							lenTcpData  = lenTcpData  - 1
						if element > 0: 
							sumData3 = sumData3 + element
					mergedTcpAveData = sumData3 / lenTcpData
					sumData3 = 0
#Putting everthing into a new line
					Newline = line.split(',')[0] + ',' + line.split(',')[1] + " " + line2.split(',')[1] + ',' + str(mergedPingAveData) + ',' + line.split(',')[3] + " " + line2.split(',')[3] + ',' + str(mergedUdpAveData) + ',' + line.split(',')[5] + " " + line2.split(',')[5] + ','+ str(mergedTcpAveData) + '\n'
					merge1NextIndex = merge2Index+1

#Creating plotting data


#Prints existing data from line1 if not equal (no merge)
				else :					
					if combineFlag == 0: #Prevents  Newline from overide
						Newline = line
					merge1NextIndex = merge2Index				
					break

#Gets data for first and last distance "Corner cases"
			else: 
				if merge1Index == 0 or merge2Index == len(merge2linesperf)-1:  #i.e first line or last line
					if combineFlag == 0:
						Newline = line	

		
		with open(outputextractperfsortedmerged, "a") as perfsortedmergedfile:
			perfsortedmergedfile.write(Newline)
		perfsortedmergedfile.close()


#Merge data (sup) based on distacce (every distance only have 1 row) - save as different file ; orig, sorted, merge sorted file 

print "INFO: SORT AND MERGE SUP\n"


#Opens output file and sorts according to distance
with open(outputextractsup , 'r') as data:
	data = csv.reader(data,delimiter=',')
	data.next()
	list1 = sorted(data, key=lambda x: (float(x[0])))

#Creates new file "output_sorted"
with open(outputextractsupsorted, "wb") as f:
	fileWriter = csv.writer(f, delimiter=',')
	writer = csv.DictWriter(f, fieldnames = ["Distance", "TxSectorData", "Frequent TxSectorData", "RxSectorData", "Frequent RxSectorData",  "SNRData", "Average SNRData" , "RemoteSNRData" , "Average RemoteSNRData" , "RSSIData" , "Average RSSIData"], delimiter = ',' )
	writer.writeheader()
	for row in list1:
		fileWriter.writerow(row)
f.close()

#Start merging same distances (sup)

with open(outputextractsupsorted, "r") as merge1sup:
	merge1linessup = merge1sup.readlines()[1:]
	merge2linessup = merge1linessup

merge1Index = -1
merge1NextIndex = 1
TxSectorDataList = []
RxSectorDataList = []
SNRDataList = []
RemoteSNRDataList = []
RSSIDataList = []

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
#Find new frequent for TxSectorData
					txsectorData = line.split(',')[1] + " " + line2.split(',')[1]
					txsectorData = txsectorData.split()
					lentxsectorData = len(txsectorData)

					# Expand values then compress after
					for element in txsectorData:
						txsectorDataval = element.split('(')[0]
						txsectorDatavalcount = int(element.split('(')[1].split(')')[0])
						for index_i in range(txsectorDatavalcount):
							TxSectorDataList.append(txsectorDataval)

					# get counts for each unique value
					a = TxSectorDataList
					aCount = {x:a.count(x) for x in a}
					#valuesA = sorted(aCount.values())
					countA = sorted(aCount, key=aCount.get)
					mostFrequentTxSectorData = countA[-1]

					# sort list in ascending order
					TxSectorDataCountSorted = sorted(aCount.items(), key = lambda x:int(x[0]))
					#formats everthing
					TxSectorDataCountFormatted = str(TxSectorDataCountSorted).strip('[]')
					TxSectorDataCountFormatted = TxSectorDataCountFormatted.replace("('","")
					TxSectorDataCountFormatted = TxSectorDataCountFormatted.replace("', ","(")
					TxSectorDataCountFormatted = TxSectorDataCountFormatted.replace(",","")



#Steps repeated for rest of RxSector, SNR, RemoteSNR, RRSI

#Find new frequent for RxSectorData
					rxsectorData = line.split(',')[3] + " " + line2.split(',')[3]
					rxsectorData = rxsectorData.split()
					lenrxsectorData = len(rxsectorData)

					# Expand values then compress after
					for element in rxsectorData:
						rxsectorDataval = element.split('(')[0]
						rxsectorDatavalcount = int(element.split('(')[1].split(')')[0])
						for index_i in range(rxsectorDatavalcount):
							RxSectorDataList.append(rxsectorDataval)

					b = RxSectorDataList
					bCount = {xx:b.count(xx) for xx in b}
					countB = sorted(bCount, key=bCount.get)
					mostFrequentRxSectorData = countB[-1]

					RxSectorDataCountSorted = sorted(bCount.items(), key = lambda x:int(x[0]))

					RxSectorDataCountFormatted = str(RxSectorDataCountSorted).strip('[]')
					RxSectorDataCountFormatted = RxSectorDataCountFormatted.replace("('","")
					RxSectorDataCountFormatted = RxSectorDataCountFormatted.replace("', ","(")
					RxSectorDataCountFormatted = RxSectorDataCountFormatted.replace(",","")

#Find new average for snrData
					snrData = line.split(',')[5] + " " + line2.split(',')[5]
					snrData = snrData.split()
					lensnrData = len(snrData)
					#print snrData

					# Expand values then compress after
					for element in snrData:
						snrDataval = element.split('(')[0]
						snrDatavalcount = int(element.split('(')[1].split(')')[0])
						for index_i in range(snrDatavalcount):
							SNRDataList.append(snrDataval)

					c = SNRDataList

					snrDatalistlength = len(SNRDataList)

					for elements in SNRDataList:
						TotalSNR2 = TotalSNR2 + float(elements)
					AverageSNRData2 = TotalSNR2 / snrDatalistlength
					AverageSNRData2 = AverageSNRData2 / 8                           # AverageSNRData2 divided by 8 on purpose

					cCount = {xxx:c.count(xxx) for xxx in c}
					countC = sorted(cCount, key=cCount.get)
					mostFrequentSNRData = countC[-1]

					SNRDataDataCountSorted = sorted(cCount.items(), key = lambda x:int(x[0]))

					SNRDataDataCountFormatted = str(SNRDataDataCountSorted).strip('[]')
					SNRDataDataCountFormatted = SNRDataDataCountFormatted.replace("('","")
					SNRDataDataCountFormatted = SNRDataDataCountFormatted.replace("', ","(")
					SNRDataDataCountFormatted = SNRDataDataCountFormatted.replace(",","")

#Find new average for remotesnrData
					remotesnrData = line.split(',')[7] + " " + line2.split(',')[7]
					remotesnrData = remotesnrData.split()
					lanremotesnrData = len(remotesnrData)

					# Expand values then compress after
					for element in remotesnrData:
						remotesnrDataval = element.split('(')[0]
						remotesnrDatavalcount = int(element.split('(')[1].split(')')[0])
						for index_i in range(remotesnrDatavalcount):
							RemoteSNRDataList.append(remotesnrDataval)

					d = RemoteSNRDataList

					remotesnrDatalistlength = len(RemoteSNRDataList)

					for elements in RemoteSNRDataList:
						TotalRemoteSNR2 = TotalRemoteSNR2 + float(elements)
					AverageRemoteSNRData2 = TotalRemoteSNR2 / remotesnrDatalistlength
					AverageRemoteSNRData2 = AverageRemoteSNRData2 / 8               # AverageRemoteSNRData2 divided by 8 on purpose

					dCount = {xxxx:d.count(xxxx) for xxxx in d}
					countD = sorted(dCount, key=dCount.get)
					mostFrequentRemoteSNRData = countD[-1]

					RemoteSNRDataCountSorted = sorted(dCount.items(), key = lambda x:int(x[0]))

					RemoteSNRDataCountFormatted = str(RemoteSNRDataCountSorted).strip('[]')
					RemoteSNRDataCountFormatted = RemoteSNRDataCountFormatted.replace("('","")
					RemoteSNRDataCountFormatted = RemoteSNRDataCountFormatted.replace("', ","(")
					RemoteSNRDataCountFormatted = RemoteSNRDataCountFormatted.replace(",","")

#Find new average for rssiData
					rssiData = line.split(',')[9] + " " + line2.split(',')[9]
					rssiData = rssiData.split()
					lenrssiData = len(rssiData)

					# Expand values then compress after
					for element in rssiData:
						rssiDataval = element.split('(')[0]
						rssiDatavalcount = int(element.split('(')[1].split(')')[0])
						for index_i in range(rssiDatavalcount):
							RSSIDataList.append(rssiDataval)

					e = RSSIDataList

					rssiDatalistlength = len(RSSIDataList)

					for elements in RSSIDataList:
						TotalRSSI2 = TotalRSSI2 + float(elements)
					AverageRSSIData2 = TotalRSSI2 / rssiDatalistlength

					eCount = {xxxxx:e.count(xxxxx) for xxxxx in e}
					countE = sorted(eCount, key=eCount.get)
					mostFrequentRSSIData = countE[-1]

					RSSIDataCountSorted = sorted(eCount.items(), key = lambda x:int(x[0]))

					RSSIDataCountFormatted = str(RSSIDataCountSorted).strip('[]')
					RSSIDataCountFormatted = RSSIDataCountFormatted.replace("('","")
					RSSIDataCountFormatted = RSSIDataCountFormatted.replace("', ","(")
					RSSIDataCountFormatted = RSSIDataCountFormatted.replace(",","")

					TotalRSSI2 = 0.0
					TotalSNR2 = 0.0
					TotalRemoteSNR2 = 0.0

# #Putting everthing into a new line
					Newline = line.split(',')[0] + ','+ TxSectorDataCountFormatted + "," + mostFrequentTxSectorData + "," + RxSectorDataCountFormatted + "," + mostFrequentRxSectorData + "," + SNRDataDataCountFormatted + "," + str(AverageSNRData2) + "," + RemoteSNRDataCountFormatted + "," + str(AverageRemoteSNRData2) + "," + RSSIDataCountFormatted + "," + str(AverageRSSIData2) + "\n"
					merge1NextIndex = merge2Index+1

					#Resets list
					TxSectorDataList = []
					RxSectorDataList = []
					SNRDataList = []
					RemoteSNRDataList = []
					RSSIDataList = []


# #Prints existing data from line1 if not equal (no merge)
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
						TxSectorDataList = []
						RxSectorDataList = []
						SNRDataList = []
						RemoteSNRDataList = []
						RSSIDataList = []
		
		with open(outputextractsupsortedmerged, "a") as supsortedmergedfile:
			supsortedmergedfile.write(Newline)
		supsortedmergedfile.close()

# Combine sup and perf output files and keep only avg/freq values
with open(outputextractsupsortedmerged, "r") as outputsupfile:
	outputsuplines = outputsupfile.readlines()[1:]
outputsupfile.close()

with open(outputextractperfsortedmerged, "r") as outputperffile:
	outputperflines = outputperffile.readlines()[1:]
outputperffile.close()

intermediatelist=[]

with open(outputextractsupperfsortedmerged, "a") as outputsupperffile:	
	for index_i in range(len(outputsuplines)):		
		intermediatelist.append(outputsuplines[index_i][:-2].split(',')+outputperflines[index_i][:-2].split(',')) #note: -2 to remove \r\n

		# remove unneeded columns
		intermediatelist[index_i].pop(16)
		intermediatelist[index_i].pop(14)
		intermediatelist[index_i].pop(12)
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

#Creating lists for other plots
TxSectorDataList3 = []
txsectorDataMostAvgPlotlist = []
RxSectorDataList3 = []
RxsectorDataMostAvgPlotlist = []
SNRDataList3 = []
SNRDataMostAvgPlotlist = []
RemoteSNRDataList3 = []
RemoteSNRDataMostAvgPlotlist = []
RSSIDataList3 = []
RSSIDataMostAvgPlotlist = []


print "INFO: GRAPHING SUP\n"

for line in outputsuplines:
	xaxisGraph = line.split(',')[0]

	#Getting Data for TxSector
	txsectorData = line.split(',')[1]
	txsectorData = txsectorData.split()
	lentxsectorData = len(txsectorData)
	txsectorDataMostAvgPlot = line.split(',')[2]
	txsectorDataMostAvgPlotlist = txsectorDataMostAvgPlotlist + [txsectorDataMostAvgPlot]

	# Expand values 
	for element in txsectorData:
		txsectorDataval = element.split('(')[0]
		txsectorDatavalcount = int(element.split('(')[1].split(')')[0])
		for index_i in range(txsectorDatavalcount):
			TxSectorDataList3.append(txsectorDataval)


	TxSectorDataList3len = len(TxSectorDataList3)


	plotDistance5 = np.zeros(TxSectorDataList3len)

	for l in range(TxSectorDataList3len):
		plotDistance5[l] = xaxisGraph

	plt.figure(5)
	for index_i in range(len(TxSectorDataList3)):
			if float(TxSectorDataList3[index_i]) < 0:
				plt.scatter(plotDistance5[index_i], TxSectorDataList3[index_i], s = 120, marker="+",color='grey')
			else:
				plt.scatter(plotDistance5[index_i], TxSectorDataList3[index_i], s = 120, marker="+",color='blue')
	plt.scatter(xaxisGraph, txsectorDataMostAvgPlot, s= 50, color='red',marker="x")
	


	TxSectorDataList3 = []



	#Getting Data for RxSectorData
	RxsectorData = line.split(',')[3]
	RxsectorData = RxsectorData.split()
	lenRxsectorData = len(RxsectorData)
	RxsectorDataMostAvgPlot = line.split(',')[4]
	RxsectorDataMostAvgPlotlist = RxsectorDataMostAvgPlotlist + [RxsectorDataMostAvgPlot]

	# Expand values 
	for element in RxsectorData:
		RxsectorDataval = element.split('(')[0]
		RxsectorDatavalcount = int(element.split('(')[1].split(')')[0])
		for index_i in range(RxsectorDatavalcount):
			RxSectorDataList3.append(RxsectorDataval)

	RxSectorDataList3len = len(RxSectorDataList3)


	plotDistance6 = np.zeros(RxSectorDataList3len)

	for l in range(RxSectorDataList3len):
		plotDistance6[l] = xaxisGraph

	plt.figure(6)
	for index_i in range(len(RxSectorDataList3)):
			if float(RxSectorDataList3[index_i]) < 0:
				plt.scatter(plotDistance6[index_i], RxSectorDataList3[index_i], s = 120, marker="+",color='grey')
			else:
				plt.scatter(plotDistance6[index_i], RxSectorDataList3[index_i], s = 120, marker="+",color='blue')
	plt.scatter(xaxisGraph, RxsectorDataMostAvgPlot, s= 50, color='red',marker="x")


	RxSectorDataList3 = []


	#Getting Data for SNRData
	SNRData = line.split(',')[5]
	SNRData = SNRData.split()
	lenSNRData = len(SNRData)
	SNRDataMostAvgPlot = line.split(',')[6]
	SNRDataMostAvgPlotlist = SNRDataMostAvgPlotlist + [SNRDataMostAvgPlot]

	# Expand values 
	for element in SNRData:
		SNRDataval = element.split('(')[0]
		SNRDatavalcount = int(element.split('(')[1].split(')')[0])
		for index_i in range(SNRDatavalcount):
			SNRDataList3.append(SNRDataval)

	SNRDataList3len = len(SNRDataList3)


	plotDistance7 = np.zeros(SNRDataList3len)

	for l in range(SNRDataList3len):
		plotDistance7[l] = xaxisGraph

	plt.figure(7)

	plt.subplot(212)
	plt.axhline(y=0, color='grey',linestyle=':')
	plt.axhline(y=200, color='yellow',linestyle=':')
	plt.axhline(y=-200, color='yellow',linestyle=':')

	linevaluetop = np.zeros(len(listxaxis2))
	linevaluebottom = np.zeros(len(listxaxis2))
	for l in range(len(listxaxis2)):
		linevaluetop[l] = 200
		linevaluebottom[l] = -200


	plt.fill_between(listxaxis2,linevaluetop,linevaluebottom, color='yellow', alpha = 0.2)

	plt.subplot(211)
	for index_i in range(len(SNRDataList3)):
			if float(SNRDataList3[index_i]) < 0:
				plt.scatter(plotDistance7[index_i], SNRDataList3[index_i], s = 120, marker="+",color='grey')
			else:
				plt.scatter(plotDistance7[index_i], SNRDataList3[index_i], s = 120, marker="+",color='blue')
	plt.scatter(xaxisGraph, SNRDataMostAvgPlot, s= 50, color='red',marker="x")


	plt.subplot(212)
	for index_i in range(len(SNRDataList3)):
			if float(SNRDataList3[index_i]) < 0:
				plt.scatter(plotDistance7[index_i], SNRDataList3[index_i], s = 120, marker="+",color='grey')
			else:
				plt.scatter(plotDistance7[index_i], SNRDataList3[index_i], s = 120, marker="+",color='blue')
	plt.scatter(xaxisGraph, SNRDataMostAvgPlot, s= 50, color='red',marker="x")


	SNRDataList3 = []







	#Getting RemoteSNRData 
	RemoteSNRData = line.split(',')[7]
	RemoteSNRData = RemoteSNRData.split()
	lenRemoteSNRData = len(RemoteSNRData)
	RemoteSNRDataMostAvgPlot = line.split(',')[8]
	RemoteSNRDataMostAvgPlotlist = RemoteSNRDataMostAvgPlotlist + [RemoteSNRDataMostAvgPlot]

	# Expand values 
	for element in RemoteSNRData:
		RemoteSNRDataval = element.split('(')[0]
		RemoteSNRDatavalcount = int(element.split('(')[1].split(')')[0])
		for index_i in range(RemoteSNRDatavalcount):
			RemoteSNRDataList3.append(RemoteSNRDataval)

	RemoteSNRDataList3len = len(RemoteSNRDataList3)


	plotDistance8 = np.zeros(RemoteSNRDataList3len)

	for l in range(RemoteSNRDataList3len):
		plotDistance8[l] = xaxisGraph

	plt.figure(8)

	plt.subplot(212)
	plt.axhline(y=0, color='grey',linestyle=':')
	plt.axhline(y=200, color='yellow',linestyle=':')
	plt.axhline(y=-200, color='yellow',linestyle=':')

	linevaluetop = np.zeros(len(listxaxis2))
	linevaluebottom = np.zeros(len(listxaxis2))
	for l in range(len(listxaxis2)):
		linevaluetop[l] = 200
		linevaluebottom[l] = -200


	plt.fill_between(listxaxis2,linevaluetop,linevaluebottom, color='yellow', alpha = 0.2)

	plt.subplot(211)
	for index_i in range(len(RemoteSNRDataList3)):
			if float(RemoteSNRDataList3[index_i]) < 0:
				plt.scatter(plotDistance8[index_i], RemoteSNRDataList3[index_i], s = 120, marker="+",color='grey')
			else:
				plt.scatter(plotDistance8[index_i], RemoteSNRDataList3[index_i], s = 120, marker="+",color='blue')
	plt.scatter(xaxisGraph,RemoteSNRDataMostAvgPlot, s= 50, color='red',marker="x")


	plt.subplot(212)
	for index_i in range(len(RemoteSNRDataList3)):
			if float(RemoteSNRDataList3[index_i]) < 0:
				plt.scatter(plotDistance8[index_i], RemoteSNRDataList3[index_i], s = 120, marker="+",color='grey')
			else:
				plt.scatter(plotDistance8[index_i], RemoteSNRDataList3[index_i], s = 120, marker="+",color='blue')
	plt.scatter(xaxisGraph, RemoteSNRDataMostAvgPlot, s= 50, color='red',marker="x")


	RemoteSNRDataList3 = []


	#Getting RSSIData

	RSSIData = line.split(',')[9]
	RSSIData = RSSIData.split()
	lenRSSIData = len(RSSIData)
	RSSIDataMostAvgPlot = line.split(',')[10]
	RSSIDataMostAvgPlotlist = RSSIDataMostAvgPlotlist + [RSSIDataMostAvgPlot]

	# Expand values 
	for element in RSSIData:
		RSSIDataval = element.split('(')[0]
		RSSIDatavalcount = int(element.split('(')[1].split(')')[0])
		for index_i in range(RSSIDatavalcount):
			RSSIDataList3.append(RSSIDataval)

	RSSIDataList3len = len(RSSIDataList3)


	plotDistance9 = np.zeros(RSSIDataList3len)

	for l in range(RSSIDataList3len):
		plotDistance9[l] = xaxisGraph

	plt.figure(9)
	for index_i in range(len(RSSIDataList3)):
			if float(RSSIDataList3[index_i]) >= 0:
				plt.scatter(plotDistance9[index_i], RSSIDataList3[index_i], s = 120, marker="+",color='grey')
			else:
				plt.scatter(plotDistance9[index_i], RSSIDataList3[index_i], s = 120, marker="+",color='blue')
	plt.scatter(xaxisGraph, RSSIDataMostAvgPlot, s= 50, color='red',marker="x")


	RSSIDataList3 = []









print "INFO: GRAPHING PERF\n"


# Prepare to plot perf data
with open(outputextractperfsortedmerged, "rt") as merged2:
	merged2lines = merged2.readlines()[1:]
	for line in merged2lines:
		xaxis2 = float(line.split(",")[0]) #find x axis
		pingDataPlot = str(line.split(",")[1])
		pingAvgDataPlot = str(line.split(",")[2])
		udpDataPlot = str(line.split(",")[3])
		udpAvgDataPlot = str(line.split(",")[4])
		tcpDataPlot = str(line.split(",")[5])
		tcpAvgDataPlot = str(line.split(",")[6])

		udpAvgDataPlotLIST = udpAvgDataPlotLIST + [udpAvgDataPlot]
		tcpAvgDataPlotLIST = tcpAvgDataPlotLIST + [tcpAvgDataPlot]
		pingAvgDataPlotLIST = pingAvgDataPlotLIST + [pingAvgDataPlot]
		listxaxis2 = listxaxis2 + [xaxis2]

		udpDataPlotsplit = udpDataPlot.split()
		udpDataPlotlen = len(udpDataPlotsplit)

		tcpDataPlotsplit = tcpDataPlot.split()
		tcpDataPlotlen = len(tcpDataPlotsplit)

		pingDataPlotsplit = pingDataPlot.split()
		pingDataPlotlen = len(pingDataPlotsplit)


#Creates array for xaxis
		plotDistance3 = np.zeros(udpDataPlotlen)
		plotDistance4 = np.zeros(tcpDataPlotlen)
		plotDistance12 = np.zeros(pingDataPlotlen)
		

	
#Fills array with xaxis
		for l in range(udpDataPlotlen):
			plotDistance3[l] = xaxis2
		for m in range(tcpDataPlotlen):
			plotDistance4[m] = xaxis2	
		for n in range(pingDataPlotlen):
			plotDistance12[n] = xaxis2

#Plots data: Adjust settings here
		plt.figure(3)	
		for index_i in range(len(udpDataPlotsplit)):
			if float(udpDataPlotsplit[index_i]) < 0:
				plt.scatter(plotDistance3[index_i], udpDataPlotsplit[index_i], s = 120, marker="+",color='grey')
			else:
				plt.scatter(plotDistance3[index_i], udpDataPlotsplit[index_i], s = 120, marker="+",color='blue')
		#plt.scatter(plotDistance3, udpDataPlotsplit, s = 120, marker="+")
		plt.scatter(xaxis2, udpAvgDataPlot, s= 50, color='red',marker="x")

		plt.figure(4)
		for index_i in range(len(tcpDataPlotsplit)):
			if float(tcpDataPlotsplit[index_i]) < 0:
				plt.scatter(plotDistance4[index_i], tcpDataPlotsplit[index_i], s = 120, marker="+",color='grey')
			else:
				plt.scatter(plotDistance4[index_i], tcpDataPlotsplit[index_i], s = 120, marker="+",color='blue')
		plt.scatter(xaxis2, tcpAvgDataPlot, s=50, color='red',marker="x" )


		plt.figure(12)
		for index_i in range(len(pingDataPlotsplit)):
			if float(pingDataPlotsplit[index_i]) < 0:
				plt.scatter(plotDistance12[index_i], pingDataPlotsplit[index_i], s = 120, marker="+",color='grey')
			else:
				plt.scatter(plotDistance12[index_i], pingDataPlotsplit[index_i], s = 120, marker="+",color='blue')
		plt.scatter(xaxis2, pingAvgDataPlot, s=50, color='red',marker="x" )


N=50
colors = np.random.rand(N)


inputlogfilename = inputlogfilename[:-4]

#Set graph
plt.figure(3)
plt.gca().set_xlim(left=0)
plt.xlabel('Distance')
plt.ylabel('Udp_Bandwidth')
plt.title('Distance(m) v Udp_Bandwidth(Mbps)',fontweight="bold")
plt.axhline(y=0, color='grey',linestyle=':')
plt.axhline(y=1000, color='green',linestyle=':')
plt.plot(listxaxis2, udpAvgDataPlotLIST, "-", color = "red")
red_line = mlines.Line2D( [], [], color='red' , marker='x', markersize=10, label='Avg Bandwidth')
Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='Bandwidth', linewidth = 0)
lgd = plt.legend(handles=[red_line,Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_dist_vs_udp_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_perf_udp_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

# plt.figure(3)
# plt.plot(listxaxis2, udpAvgDataPlotLIST, "-o")


plt.figure(4)
plt.gca().set_xlim(left=0)
plt.xlabel('Distance')
plt.ylabel('Tcp_Bandwidth')
plt.title('Distance(m) v Tcp_Bandwidth(Mbps)',fontweight="bold")
plt.axhline(y=0, color='grey',linestyle=':')
plt.axhline(y=1000, color='green',linestyle=':')
plt.plot(listxaxis2, tcpAvgDataPlotLIST, "-", color = "red")
red_line = mlines.Line2D( [], [], color='red' , marker='x', markersize=10, label='Avg Bandwidth')
Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='Bandwidth', linewidth = 0)
lgd = plt.legend(handles=[red_line,Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_dist_vs_tcp_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_perf_tcp_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')


plt.figure(12)
plt.gca().set_xlim(left=0)
plt.xlabel('Distance')
plt.ylabel('Ping')
plt.title('Distance(m) v Ping',fontweight="bold")
plt.axhline(y=0, color='grey',linestyle=':')
plt.plot(listxaxis2, pingAvgDataPlotLIST, "-", color = "red")
red_line = mlines.Line2D( [], [], color='red' , marker='x', markersize=10, label='Avg Ping')
Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='Ping', linewidth = 0)
lgd = plt.legend(handles=[red_line,Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_dist_vs_udp_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_perf_ping_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')



plt.figure(5)
plt.gca().set_xlim(left=0)
plt.xlabel('Distance')
plt.ylabel('TxSectorData')
plt.title('Distance(m) v TxSectorData',fontweight="bold")
plt.axhline(y=0, color='grey',linestyle=':')
#plt.axhline(y=1000, color='green',linestyle=':')
plt.plot(listxaxis2, txsectorDataMostAvgPlotlist, "-", color = "red")
red_line = mlines.Line2D( [], [], color='red' , marker='x', markersize=10, label='Most Frequent TxSectorData')
Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='TxSectorData', linewidth = 0)
lgd = plt.legend(handles=[red_line,Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_dist_vs_txsector_data"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_sup_txsector_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')


plt.figure(6)
plt.gca().set_xlim(left=0)
plt.xlabel('Distance')
plt.ylabel('RxSectorData')
plt.title('Distance(m) v RxSectorData',fontweight="bold")
plt.axhline(y=0, color='grey',linestyle=':')
#plt.axhline(y=1000, color='green',linestyle=':')
plt.plot(listxaxis2, RxsectorDataMostAvgPlotlist, "-", color = "red")
red_line = mlines.Line2D( [], [], color='red' , marker='x', markersize=10, label='Most Frequent RxSectorData')
Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='RxSectorData', linewidth = 0)
lgd = plt.legend(handles=[red_line,Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_dist_vs_Rxsector_data"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_sup_rxsector_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')


#
plt.figure(9)
plt.gca().set_xlim(left=0)
plt.xlabel('Distance')
plt.ylabel('RSSIData')
plt.title('Distance(m) v RSSIData',fontweight="bold")
plt.axhline(y=0, color='grey',linestyle=':')
#plt.axhline(y=1000, color='green',linestyle=':')
plt.plot(listxaxis2, RSSIDataMostAvgPlotlist, "-", color = "red")
red_line = mlines.Line2D( [], [], color='red' , marker='x', markersize=10, label='Average RSSIData')
Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='RSSIData', linewidth = 0)
lgd = plt.legend(handles=[red_line,Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_dist_vs_RSSI_data"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_sup_rssi_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')



#Adjusting SNRData plots (Part 1)

plt.figure(7)
plt.subplot(211)
plt.axhline(y=0, color='grey',linestyle=':')
plt.axhline(y=200, color='yellow',linestyle=':')
plt.axhline(y=-200, color='yellow',linestyle=':')

linevaluetop = np.zeros(len(listxaxis2))
linevaluebottom = np.zeros(len(listxaxis2))
for l in range(len(listxaxis2)):
	linevaluetop[l] = 200
	linevaluebottom[l] = -200


plt.fill_between(listxaxis2,linevaluetop,linevaluebottom, color='yellow')




# #Adjusting SNRData plots (Part 1)

plt.figure(7)
plt.subplot(211)

linevaluetop = np.zeros(len(listxaxis2))
linevaluebottom = np.zeros(len(listxaxis2))
for l in range(len(listxaxis2)):
	linevaluetop[l] = 200
	linevaluebottom[l] = -200

plt.gca().set_xlim(left=0)
plt.ylabel('SNRData')
plt.title('Distance(m) v SNRData (Full)',fontweight="bold")
plt.axhline(y=0, color='grey',linestyle=':')


#plt.axhline(y=1000, color='green',linestyle=':')


plt.plot(listxaxis2, SNRDataMostAvgPlotlist, "-", color = "red")
red_line = mlines.Line2D( [], [], color='red' , marker='x', markersize=10, label='Average SNRData Div 8')
Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='SNRData', linewidth = 0)
lgd = plt.legend(handles=[red_line,Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-1.42))


plt.subplot(212)
plt.axhline(y=0, color='grey',linestyle=':')
plt.axhline(y=200, color='yellow',linestyle=':')
plt.axhline(y=-200, color='yellow',linestyle=':')
plt.xlabel('Distance')

linevaluetop = np.zeros(len(listxaxis2))
linevaluebottom = np.zeros(len(listxaxis2))
for l in range(len(listxaxis2)):
	linevaluetop[l] = 200
	linevaluebottom[l] = -200


plt.fill_between(listxaxis2,linevaluetop,linevaluebottom, color='yellow', alpha = 0.1)

plt.title('Distance(m) v SNRData (Zoomed)',fontweight="bold")
plt.ylim(-200, 200)
plt.ylabel('SNRData')

plt.gca().set_xlim(left=0)
plt.plot(listxaxis2, SNRDataMostAvgPlotlist, "-", color = "red")
#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_dist_vs_SNR_data"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_sup_snr_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')





#Adjusting RemoteSNRData plots (Part 1)

plt.figure(8)
plt.subplot(211)
plt.axhline(y=0, color='grey',linestyle=':')
plt.axhline(y=200, color='yellow',linestyle=':')
plt.axhline(y=-200, color='yellow',linestyle=':')

linevaluetop = np.zeros(len(listxaxis2))
linevaluebottom = np.zeros(len(listxaxis2))
for l in range(len(listxaxis2)):
	linevaluetop[l] = 200
	linevaluebottom[l] = -200


plt.fill_between(listxaxis2,linevaluetop,linevaluebottom, color='yellow')




# #Adjusting RemoteSNRData plots (Part 1)

plt.figure(8)
plt.subplot(211)

linevaluetop = np.zeros(len(listxaxis2))
linevaluebottom = np.zeros(len(listxaxis2))
for l in range(len(listxaxis2)):
	linevaluetop[l] = 200
	linevaluebottom[l] = -200

plt.gca().set_xlim(left=0)
plt.ylabel('RemoteSNRData')
plt.title('Distance(m) v RemoteSNRData (Full)' , fontweight="bold")
plt.axhline(y=0, color='grey',linestyle=':')


#plt.axhline(y=1000, color='green',linestyle=':')

plt.plot(listxaxis2, RemoteSNRDataMostAvgPlotlist, "-", color = "red")
red_line = mlines.Line2D( [], [], color='red' , marker='x', markersize=10, label='Average RemoteSNRData Div 8')
Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='RemoteSNRData', linewidth = 0)
lgd = plt.legend(handles=[red_line,Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-1.51), fontsize=10)


plt.subplot(212)
plt.axhline(y=0, color='grey',linestyle=':')
plt.axhline(y=200, color='yellow',linestyle=':')
plt.axhline(y=-200, color='yellow',linestyle=':')
plt.xlabel('Distance')

linevaluetop = np.zeros(len(listxaxis2))
linevaluebottom = np.zeros(len(listxaxis2))
for l in range(len(listxaxis2)):
	linevaluetop[l] = 200
	linevaluebottom[l] = -200


plt.fill_between(listxaxis2,linevaluetop,linevaluebottom, color='yellow', alpha = 0.1)

plt.title('Distance(m) v RemoteSNRData (Zoomed)',fontweight="bold")
plt.ylim(-200, 200)
plt.ylabel('RemoteSNRData')

plt.gca().set_xlim(left=0)
plt.plot(listxaxis2, RemoteSNRDataMostAvgPlotlist, "-", color = "red")
#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_dist_vs_RemoteSNR_data"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_sup_remoteSNR_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')



# Remove temp files
try:
	os.remove(outputextractsup)
except:
	donothing=1	
try:
	os.remove(outputextractsupsorted)
except:
	donothing=1	
try:
	os.remove(outputextractperf)
except:
	donothing=1				
try:
	os.remove(outputextractperfsorted)
except:
	donothing=1							

