import sys, math
import numpy as np
import matplotlib.pyplot as plt
import csv, itertools , xlwt ,operator
import pandas as pd
from collections import OrderedDict
import os
import matplotlib.lines as mlines
import gps
import time
import math as m
from math import sin ,cos,sqrt ,atan2 , radians

SKIPFIRSTREADING = 1 # set to 1 to ignore first measurement (note: sometimes first readings are significantly worse)

####### Plot or skip plo t#######
SKIPPLOT_PING = 1
SKIPPLOT_UDP = 0
SKIPPLOT_TCP = 0


SKIPPLOT_TXSECTOR = 0
SKIPPLOT_RXSECTOR = 1
SKIPPLOT_SNR = 1
SKIPPLOT_REMOTESNR = 0
SKIPPLOT_RSSI = 0
SKIPPLOT_TXMCS = 0


SKIPPLOT_BESTBEAMSNR = 1
SKIPPLOT_LASTREMOTERSSI = 1
SKIPPLOT_LASTBEACONRSSI = 1
SKIPPLOT_LASTDATARSSI = 1
SKIPPLOT_CURRENTMCS = 1
SKIPPLOT_RFTEMP = 1
SKIPPLOT_BBTEMP = 1
#################################

#list of data
TxSectordataList = []
RxSectordataList = []
SNRdataList = []
RemoteSNRdataList = []
RSSIdataList = []
TxMCSList = []
timestamplist = []

startSupKeyWord = str("PING")
pingTime = str("time=")
pingdatalist = []
timestamplist2 = []
avgPing = float()

SortingKeyWord = str("Gbits/sec")
SortingKeyWord2 = str("Mbits/sec")
SortingKeyWord3 = str("Kbits/sec")
keep_phrases = ["bits/sec"]
myKeyWord = str("---------------")
importantudp = []
importanttcp = []
timestamplist3 = []
timestamplist4 = []
listTcpValue = []
valueAvgTcp = []
valueAvgUdp = float()
valueAvgTcp = float()
listUdpValue = []

timestamplist5 = []
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

TIMESTAMPLENGTH = 17 # hardcoded!

#gps connections lists and words
keyword = ["BESTPOSA"]
distancelist = []
timestampgpslist = []

lat1 = m.radians(1.322759)
lon1 = m.radians(103.931371)
# approximate radius of earth in km
R = 6373.0


def twos_comp(val, bits): #"""compute the 2's complement of int value val"""
	if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
		val = val - (1 << bits)        # compute negative value
	return val                         # return positive value as is


def hex_to_dex(strng_of_hex):
	return int(strng_of_hex, 16)


## main
print "INFO: START LIVE EXTRACT PLOT\n"

# Get log file name and check if valid
if len(sys.argv) != 2:
	print "Correct usage: python extractplot<ver>.py [dir]/[filename].csv"
	quit() # not valid so exit

if SKIPFIRSTREADING  == 1:
	#print "Note: Skip first reading: Enabled (to avoid abnormal values)"
	donothing = 1

inputlogfile = sys.argv[1]
# inputlogfiledir = os.path.dirname(os.path.realpath(inputlogfile)) + "/"
inputlogfiledir = str(inputlogfile.rsplit('/',1)[0]) + "/"
inputlogfilename = os.path.basename(inputlogfile)

#Code: plots data collected from each set of data files (sup, statsup, tcp, udp, ping)
with open(inputlogfile, "rt") as inputlog: #Input main file name
	inputlogcontent = inputlog.readlines()[1] # Reads firstline of log file
	xaxis = float(inputlogcontent.split(",")[2]) #find x axis
	udpFilePathName = inputlogfiledir + str(inputlogcontent.split(",")[11]) #find udp files
	pingFilePathName = inputlogfiledir + str(inputlogcontent.split(",")[10]) #finds ping file
	tcpFilePathName = inputlogfiledir + str(inputlogcontent.split(",")[12]) #find tcp files
	supFilePathName = inputlogfiledir + str(inputlogcontent.split(",")[8]) #find sup files
	statFilePathName = inputlogfiledir + str(inputlogcontent.split(",")[14]) #find sup files
	#tcpFilePathName = tcpFilePathName.rstrip() (Needed for if tcp file is last col in csv file)
	gpsFilePathName = inputlogfiledir + str(inputlogcontent.split(",")[16]) #find sup files
	gpsFilePathName = gpsFilePathName.rstrip()

print "\nSummary:"
print "Input:"
print inputlogfile
print "Output:"
print "None"

print "INFO: PROCESSING GPS FILE\n"

try:
	gpsfile_exists = os.path.isfile(gpsFilePathName) #Checks if file is present in folder

	with open (gpsFilePathName, "rt") as gpsfile:
		logfileslines = gpsfile.readlines()

		for line in logfileslines:

			for phrase in keyword:
				if phrase in line:

					timestampgps = line.split(" ")[0]
			
					timestampgpslist = timestampgpslist + [timestampgps]

					lat2 = m.radians(float(line.split(",")[11]))            #What is the deviation?
					lon2 = m.radians(float(line.split(",")[12]))
					# print lat2
					# print lon2

					dlon = lon2 - lon1
					dlat = lat2 - lat1

					a = m.sin(dlat / 2)**2 + m.cos(lat1) * m.cos(lat2) * m.sin(dlon / 2)**2
					c = 2 * m.atan2(sqrt(a), m.sqrt(1 - a))

					distance = R * c
					distance = distance*1000 #in meter

					distancelist = distancelist + [distance]
except:
	print "WARNING (IOERROR: " + gpsFilePathName +" Tcp file not found)"
	donothing = 1



print "INFO: PROCESSING SUP FILE\n"

with open(supFilePathName, "rt") as supfile:
	supfilelines = supfile.readlines()[1:]
	for line in supfilelines:
		if "BF-EVENT-DATA:" in line:
			data = line.split(" ")[2]
			timestamp = line.split(" ")[0]



			TxSectordata = data.split(",")[0]
			RxSectordata = data.split(",")[1]
			SNRdata = float(data.split(",")[2])
			SNRdata = SNRdata/8
			RemoteSNRdata = float(data.split(",")[3])
			RemoteSNRdata = RemoteSNRdata/8
			RSSIdata = data.split(",")[4]
			TxMCS = data.split(",")[5]

			timestamplist = timestamplist + [timestamp]

			TxSectordataList = TxSectordataList + [TxSectordata]
			RxSectordataList = RxSectordataList + [RxSectordata]
			SNRdataList = SNRdataList + [SNRdata]
			RemoteSNRdataList = RemoteSNRdataList + [RemoteSNRdata]
			RSSIdataList = RSSIdataList + [RSSIdata]
			TxMCSList = TxMCSList + [TxMCS]


#Plot data onto graph (combined or separate)
if SKIPPLOT_TXSECTOR == 1:
	donothing = 1
else:
	if gpsfile_exists == True: #Plot Timestamp v TXSECTOR_distance when gps file is present
		fig,ax1 = plt.subplots()
		ax1.set_xlabel('Timestamp')
		ax1.set_ylabel('Sup Data', color= "black")
		lines, = ax1.plot(timestamplist, TxSectordataList, color="r" , marker = '+', markersize = 10)
		ax1.tick_params(axis='y', labelcolor="black")

		ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

		ax2.set_ylabel('Distance', color="b")  # we already handled the x-label with ax1
		liness, = ax2.plot(timestampgpslist, distancelist, color="b", marker = '+' , markersize = 10 , linestyle = ":")
		ax2.tick_params(axis='y', labelcolor="black")

		TxsectorDatalist_line = mlines.Line2D([], [], color='r', label='TxSector Data', linestyle = ":")
		Distancelist_line = mlines.Line2D([], [], color='b', label='Distance', linestyle = ":")

		lgd = plt.legend(handles=[TxsectorDatalist_line,Distancelist_line],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		plt.title('Timestamp v Txsector_Distance ',fontweight="bold")
	else:
		plt.figure(1)
		plt.xlabel('Timestamp')
		plt.ylabel('Sup Data')
		plt.title('Timestamp v TxSector',fontweight="bold")
		plt.plot(timestamplist, TxSectordataList, marker = "+", linestyle = ":", color = "b")
		Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='TxSector', linewidth = 0)
		lgd = plt.legend(handles=[Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_dist_vs_udp_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')
		#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_perf_udp_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

if SKIPPLOT_RXSECTOR == 1:
	donothing = 1
else:
	if gpsfile_exists == True: #Plot Timestamp v RXSECTOR_distance when gps file is present
		fig,ax1 = plt.subplots()
		ax1.set_xlabel('Timestamp')
		ax1.set_ylabel('Sup Data', color= "black")
		lines, = ax1.plot(timestamplist, RxSectordataList, color="r" , marker = '+', markersize = 10)
		ax1.tick_params(axis='y', labelcolor="black")

		ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

		ax2.set_ylabel('Distance', color="b")  # we already handled the x-label with ax1
		liness, = ax2.plot(timestampgpslist, distancelist, color="b", marker = '+' , markersize = 10 , linestyle = ":")
		ax2.tick_params(axis='y', labelcolor="black")

		RxsectorDatalist_line = mlines.Line2D([], [], color='r', label='RxSector Data', linestyle = ":")
		Distancelist_line = mlines.Line2D([], [], color='b', label='Distance', linestyle = ":")

		lgd = plt.legend(handles=[RxsectorDatalist_line,Distancelist_line],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		plt.title('Timestamp v Rxsector_Distance ',fontweight="bold")
	else:
		plt.figure(2)
		plt.xlabel('Timestamp')
		plt.ylabel('Sup Data')
		plt.title('Timestamp v RxSector',fontweight="bold")
		plt.plot(timestamplist, RxSectordataList, marker = "+", linestyle = ":", color = "b")
		Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label=' RxSector', linewidth = 0)
		lgd = plt.legend(handles=[Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_perf_udp_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

if SKIPPLOT_SNR == 1:
	donothing = 1
else:
	if gpsfile_exists == True: #Plot Timestamp v SNR_distance when gps file is present
		fig,ax1 = plt.subplots()
		ax1.set_xlabel('Timestamp')
		ax1.set_ylabel('Sup Data', color= "black")
		lines, = ax1.plot(timestamplist, SNRdataList, color="r" , marker = '+', markersize = 10)
		ax1.tick_params(axis='y', labelcolor="black")

		ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

		ax2.set_ylabel('Distance', color="b")  # we already handled the x-label with ax1
		liness, = ax2.plot(timestampgpslist, distancelist, color="b", marker = '+' , markersize = 10 , linestyle = ":")
		ax2.tick_params(axis='y', labelcolor="black")

		SNRdatalist_line = mlines.Line2D([], [], color='r', label='SNR Data', linestyle = ":")
		Distancelist_line = mlines.Line2D([], [], color='b', label='Distance', linestyle = ":")

		lgd = plt.legend(handles=[SNRdatalist_line,Distancelist_line],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		plt.title('Timestamp v SNR_Distance ',fontweight="bold")
	else:
		plt.figure(3)
		plt.xlabel('Timestamp')
		plt.ylabel('Sup Data')
		plt.title('Timestamp v SNR',fontweight="bold")
		plt.plot(timestamplist, SNRdataList, marker = "+", linestyle = ":", color = "b")
		Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='SNR', linewidth = 0)
		lgd = plt.legend(handles=[Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_perf_udp_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

if SKIPPLOT_REMOTESNR == 1:
	donothing = 1
else:
	if gpsfile_exists == True: #Plot Timestamp v REMOTESNR_distance when gps file is present
		fig,ax1 = plt.subplots()
		ax1.set_xlabel('Timestamp')
		ax1.set_ylabel('Sup Data', color= "black")
		lines, = ax1.plot(timestamplist, RemoteSNRdataList, color="r" , marker = '+', markersize = 10)
		ax1.tick_params(axis='y', labelcolor="black")

		ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

		ax2.set_ylabel('Distance', color="b")  # we already handled the x-label with ax1
		liness, = ax2.plot(timestampgpslist, distancelist, color="b", marker = '+' , markersize = 10 , linestyle = ":")
		ax2.tick_params(axis='y', labelcolor="black")

		RemoteSNRDatalist_line = mlines.Line2D([], [], color='r', label='RemoteSNR Data', linestyle = ":")
		Distancelist_line = mlines.Line2D([], [], color='b', label='Distance', linestyle = ":")

		lgd = plt.legend(handles=[RemoteSNRDatalist_line,Distancelist_line],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		plt.title('Timestamp v RemoteSNR_Distance ',fontweight="bold")
	else:
		plt.figure(4)
		plt.xlabel('Timestamp')
		plt.ylabel('Sup Data')
		plt.title('Timestamp v RemoteSNR',fontweight="bold")
		plt.plot(timestamplist, RemoteSNRdataList, marker = "+", linestyle = ":", color = "b")
		Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='RemoteSNR', linewidth = 0)
		lgd = plt.legend(handles=[Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_perf_udp_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')


if SKIPPLOT_RSSI == 1:
	donothing = 1
else:
	if gpsfile_exists == True: #Plot Timestamp v RSSI_distance when gps file is present
		fig,ax1 = plt.subplots()
		ax1.set_xlabel('Timestamp')
		ax1.set_ylabel('Sup Data', color= "black")
		lines, = ax1.plot(timestamplist, RSSIdataList, color="r" , marker = '+', markersize = 10)
		ax1.tick_params(axis='y', labelcolor="black")

		ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

		ax2.set_ylabel('Distance', color="b")  # we already handled the x-label with ax1
		liness, = ax2.plot(timestampgpslist, distancelist, color="b", marker = '+' , markersize = 10 , linestyle = ":")
		ax2.tick_params(axis='y', labelcolor="black")

		RSSIDatalist_line = mlines.Line2D([], [], color='r', label='RSSI Data', linestyle = ":")
		Distancelist_line = mlines.Line2D([], [], color='b', label='Distance', linestyle = ":")

		lgd = plt.legend(handles=[RSSIDatalist_line,Distancelist_line],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		plt.title('Timestamp v RSSI_Distance ',fontweight="bold")
	else:
		plt.figure(5)
		plt.xlabel('Timestamp')
		plt.ylabel('Sup Data')
		plt.title('Timestamp v RSSI',fontweight="bold")
		plt.plot(timestamplist, RSSIdataList, marker = "+", linestyle = ":", color = "b")
		Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='RSSI', linewidth = 0)
		lgd = plt.legend(handles=[Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_perf_udp_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

if SKIPPLOT_TXMCS == 1:
	donothing = 1
else:
	if gpsfile_exists == True: #Plot Timestamp v TXMCS_distance when gps file is present
		fig,ax1 = plt.subplots()
		ax1.set_xlabel('Timestamp')
		ax1.set_ylabel('Sup Data', color= "black")
		axes = plt.gca()
		axes.set_ylim([0,16])
		lines, = ax1.plot(timestamplist, TxMCSList, color="r" , marker = '+', markersize = 10)
		ax1.tick_params(axis='y', labelcolor="black")

		ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

		ax2.set_ylabel('Distance', color="b")  # we already handled the x-label with ax1
		liness, = ax2.plot(timestampgpslist, distancelist, color="b", marker = '+' , markersize = 10 , linestyle = ":")
		ax2.tick_params(axis='y', labelcolor="black")

		TxMCSDatalist_line = mlines.Line2D([], [], color='r', label='TxMCS Data', linestyle = ":")
		Distancelist_line = mlines.Line2D([], [], color='b', label='Distance', linestyle = ":")

		lgd = plt.legend(handles=[TxMCSDatalist_line,Distancelist_line],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		plt.title('Timestamp v TxMCS_Distance ',fontweight="bold")
	else:
		plt.figure(6)
		plt.xlabel('Timestamp')
		plt.ylabel('Sup Data')
		plt.title('Timestamp v TxMCS',fontweight="bold")
		plt.plot(timestamplist, TxMCSList, marker = "+", linestyle = ":", color = "b")
		Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='TxMCS', linewidth = 0)
		lgd = plt.legend(handles=[Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_perf_udp_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')


#Ping data already checks if file is empty
print "INFO: PROCESSING PERF FILES\n"

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
								timestamp2 = line.split(" ")[0]
								timestamplist2 = timestamplist2 + [timestamp2]

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
			# pingdatalist = pingdatalist + [pingdata]
			# timestamplist2 = timestamplist2 + [timestamp2] 

# Plot data for Ping #

if SKIPPLOT_PING == 1:
	donothing = 1
else:
	if gpsfile_exists == True: #Plot Timestamp v PING_distance when gps file is present
		fig,ax1 = plt.subplots()
		ax1.set_xlabel('Timestamp')
		plt.axhline(y=0, color='grey',linestyle=':')
		ax1.set_ylabel('Ping Data', color= "black")
		lines, = ax1.plot(timestamplist2, listPingValue, color="r" , marker = '+', markersize = 10)
		ax1.tick_params(axis='y', labelcolor="black")

		ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

		ax2.set_ylabel('Distance', color="b")  # we already handled the x-label with ax1
		liness, = ax2.plot(timestampgpslist, distancelist, color="b", marker = '+' , markersize = 10 , linestyle = ":")
		ax2.tick_params(axis='y', labelcolor="black")

		PingDatalist_line = mlines.Line2D([], [], color='r', label='Ping Data', linestyle = ":")
		Distancelist_line = mlines.Line2D([], [], color='b', label='Distance', linestyle = ":")

		lgd = plt.legend(handles=[PingDatalist_line,Distancelist_line],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		plt.title('Timestamp v Ping_Distance ',fontweight="bold")

	else:
		plt.figure(7)
		plt.xlabel('Timestamp')
		plt.ylabel('Ping Data')
		plt.axhline(y=0, color='grey',linestyle=':')
		plt.title('Timestamp v Ping',fontweight="bold")
		plt.plot(timestamplist2, listPingValue, marker = "+", linestyle = ":", color = "b")
		Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='Ping', linewidth = 0)
		lgd = plt.legend(handles=[Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		#plt.savefig(inputlogfiledir+OUTPUT_FOLDER2+"graph_perf_udp_"+inputlogfilename+".png", bbox_extra_artists=(lgd,), bbox_inches='tight')


# #TCP and UDP data already checks if file is empty

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
						timestamp3 = line.split(" ")[0]
						timestamplist3 = timestamplist3 + [timestamp3]
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
						timestamp3 = line.split(" ")[0]
						timestamplist3 = timestamplist3 + [timestamp3]		
						splitlinetcp = line.split()
						splitlen=len(splitlinetcp)
						numbertcp = float(line.split()[(splitlen-2)])
						listTcpValue += [numbertcp]
						valueAvgTcp += numbertcp
				if SortingKeyWord3 in line: #Converting to Mbits/sec from Gbits.sec
					if SKIPFIRSTREADING == 1 and skippedfirstreading == 0:
						skippedfirstreading = 1
					else:
						timestamp3 = line.split(" ")[0]
						timestamplist3 = timestamplist3 + [timestamp3]
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
						timestamp4 = line.split(" ")[0]
						timestamplist4 = timestamplist4 + [timestamp4]
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
						timestamp4 = line.split(" ")[0]
						timestamplist4 = timestamplist4 + [timestamp4]
						splitlineudp = line.partition("Mbits/sec")[0]
						splitlineudp = splitlineudp.split()
						numberudp = float(splitlineudp[-1])
						listUdpValue += [numberudp]
						valueAvgUdp += numberudp

				if SortingKeyWord3 in line:
					if SKIPFIRSTREADING == 1 and skippedfirstreading == 0:
						skippedfirstreading = 1
					else:
						timestamp4 = line.split(" ")[0]
						timestamplist4 = timestamplist4 + [timestamp4]
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

# Plot data for UDP & TCP #
if SKIPPLOT_UDP == 1:
	donothing = 1
else:
	if gpsfile_exists == True: #Plot Timestamp v UDP_distance when gps file is present
		fig,ax1 = plt.subplots()
		ax1.set_xlabel('Timestamp')
		plt.axhline(y=0, color='grey',linestyle=':')
		ax1.set_ylabel('UDP Data', color= "black")
		lines, = ax1.plot(timestamplist4, listUdpValue, color="r" , marker = '+', markersize = 10)
		ax1.tick_params(axis='y', labelcolor="black")

		ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

		ax2.set_ylabel('Distance', color="b")  # we already handled the x-label with ax1
		liness, = ax2.plot(timestampgpslist, distancelist, color="b", marker = '+' , markersize = 10 , linestyle = ":")
		ax2.tick_params(axis='y', labelcolor="black")

		UdpDatalist_line = mlines.Line2D([], [], color='r', label='Udp Data', linestyle = ":")
		Distancelist_line = mlines.Line2D([], [], color='b', label='Distance', linestyle = ":")

		lgd = plt.legend(handles=[UdpDatalist_line,Distancelist_line],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		plt.title('Timestamp v Udp_Bandwidth(Mbps)_Distance ',fontweight="bold")

	else:
		plt.figure(8)	
		plt.xlabel('Timestamp')
		plt.ylabel('UDP Data')
		plt.axhline(y=0, color='grey',linestyle=':')
		plt.axhline(y=1000, color='green',linestyle=':')
		plt.title('Timestamp v Udp_Bandwidth(Mbps)',fontweight="bold")
		plt.plot(timestamplist4, listUdpValue, marker = "+", linestyle = ":", color = "b")
		Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='bandwidth', linewidth = 0)
		lgd = plt.legend(handles=[Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))


if SKIPPLOT_TCP == 1:
	donothing = 1
else:
	if gpsfile_exists == True: #Plot Timestamp v TCP_distance when gps file is present
		fig,ax1 = plt.subplots()
		ax1.set_xlabel('Timestamp')
		plt.axhline(y=0, color='grey',linestyle=':')
		ax1.set_ylabel('TCP Data', color= "black")
		lines, = ax1.plot(timestamplist3, listTcpValue, color="r" , marker = '+', markersize = 10)
		ax1.tick_params(axis='y', labelcolor="black")

		ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

		ax2.set_ylabel('Distance', color="b")  # we already handled the x-label with ax1
		liness, = ax2.plot(timestampgpslist, distancelist, color="b", marker = '+' , markersize = 10 , linestyle = ":")
		ax2.tick_params(axis='y', labelcolor="black")

		TcpDatalist_line = mlines.Line2D([], [], color='r', label='Tcp Data', linestyle = ":")
		Distancelist_line = mlines.Line2D([], [], color='b', label='Distance', linestyle = ":")

		lgd = plt.legend(handles=[TcpDatalist_line,Distancelist_line],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		plt.title('Timestamp v Tcp_Bandwidth(Mbps)_Distance ',fontweight="bold")

	else:
		plt.figure(9)
		plt.ylabel('TCP Data')
		plt.axhline(y=0, color='grey',linestyle=':')
		plt.axhline(y=1000, color='green',linestyle=':')
		plt.title('Timestamp v Tcp_Bandwidth(Mbps)',fontweight="bold")
		plt.plot(timestamplist3, listTcpValue, marker = "+", linestyle = ":", color = "b")
		Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='bandwidth', linewidth = 0)
		lgd = plt.legend(handles=[Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))

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

print "INFO: PROCESSING STAT FILE\n"

# Note: assumed that sup file always exists and not empty
with open(statFilePathName, "rt") as statSupFile:
	statSupFilelines = statSupFile.readlines()

	# lineconnectedtrue= 0
	for line in statSupFilelines:
		TimestampLine = line.split(" ")[0]
		if len(TimestampLine) != TIMESTAMPLENGTH:
			donothing = 1
			#print "WARNING ("+statFilePathName+" has line without timestamp)"
			continue
		
		if float(TimestampLine) >= float(earliesttimestamp) and float(TimestampLine) <= float(latesttimestamp): 
			for phrases in stateventdatakeyword:
				if phrases in line and str("FAIL") not in line and line.count(',') == numberofcommas:
					dataList = line.split(" ")[2]
					timestamp5 = line.split(" ")[0]
					timestamplist5 = timestamplist5 + [timestamp5]

					BestBeamSNRData = dataList.split(',')[0]
					BestBeamSNRData = hex_to_dex(BestBeamSNRData)
					BestBeamSNRData = twos_comp(BestBeamSNRData, 8)
					BestBeamSNRDataList = BestBeamSNRDataList + [str(BestBeamSNRData)]
					TotalBestBeamSNR = TotalBestBeamSNR + float(BestBeamSNRData)

					LastRemoteRssiData = dataList.split(',')[1]
					LastRemoteRssiData = hex_to_dex(LastRemoteRssiData)
					LastRemoteRssiData = twos_comp(LastRemoteRssiData , 8)
					LastRemoteRssiDataList = LastRemoteRssiDataList + [str(LastRemoteRssiData)]
					TotalLastRemoteRssi = TotalLastRemoteRssi + float(LastRemoteRssiData)

					LastBeaconRssiData = dataList.split(',')[2]
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

#Diplaying of Stat Graph####
if SKIPPLOT_BESTBEAMSNR == 1:
	donothing = 1
else:
	if gpsfile_exists == True: #Plot Timestamp v BESTBEAMSNR_distance when gps file is present
		fig,ax1 = plt.subplots()
		ax1.set_xlabel('Timestamp')
		ax1.set_ylabel('Stat Data', color= "black")
		lines, = ax1.plot(timestamplist5, BestBeamSNRDataList, color="r" , marker = '+', markersize = 10)
		ax1.tick_params(axis='y', labelcolor="black")

		ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

		ax2.set_ylabel('Distance', color="b")  # we already handled the x-label with ax1
		liness, = ax2.plot(timestampgpslist, distancelist, color="b", marker = '+' , markersize = 10 , linestyle = ":")
		ax2.tick_params(axis='y', labelcolor="black")

		BestBeamSNRDatalist_line = mlines.Line2D([], [], color='r', label='BestBeamSNR Data', linestyle = ":")
		Distancelist_line = mlines.Line2D([], [], color='b', label='Distance', linestyle = ":")

		lgd = plt.legend(handles=[BestBeamSNRDatalist_line,Distancelist_line],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		plt.title('Timestamp v BestBeamSNR_Distance ',fontweight="bold")

	else:
		plt.figure(10)		
		plt.xlabel('Timestamp')
		plt.ylabel('Stat Data')
		plt.title('Timestamp v BestBeamSNR',fontweight="bold")
		plt.plot(timestamplist5, BestBeamSNRDataList, marker = "+", linestyle = ":", color = "b")
		Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='bestbeamsnr', linewidth = 0)
		lgd = plt.legend(handles=[Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))

if SKIPPLOT_LASTREMOTERSSI == 1:
	donothing = 1
else:
	if gpsfile_exists == True: #Plot Timestamp v LASTREMOTERSSI_distance when gps file is present
		fig,ax1 = plt.subplots()
		ax1.set_xlabel('Timestamp')
		ax1.set_ylabel('Stat Data', color= "black")
		lines, = ax1.plot(timestamplist5, LastRemoteRssiDataList, color="r" , marker = '+', markersize = 10)
		ax1.tick_params(axis='y', labelcolor="black")

		ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

		ax2.set_ylabel('Distance', color="b")  # we already handled the x-label with ax1
		liness, = ax2.plot(timestampgpslist, distancelist, color="b", marker = '+' , markersize = 10 , linestyle = ":")
		ax2.tick_params(axis='y', labelcolor="black")

		LastRemoteRssiDatalist_line = mlines.Line2D([], [], color='r', label='LastRemoteRssi Data', linestyle = ":")
		Distancelist_line = mlines.Line2D([], [], color='b', label='Distance', linestyle = ":")

		lgd = plt.legend(handles=[LastRemoteRssiDatalist_line,Distancelist_line],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		plt.title('Timestamp v LastRemoteRssi_Distance ',fontweight="bold")

	else:
		plt.figure(11)
		plt.ylabel('Stat Data')
		plt.title('Timestamp v LastRemoteRssi',fontweight="bold")
		plt.plot(timestamplist5, LastRemoteRssiDataList, marker = "+", linestyle = ":", color = "b")
		Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='lastremoterssi', linewidth = 0)
		lgd = plt.legend(handles=[Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))

if SKIPPLOT_LASTBEACONRSSI == 1:
	donothing = 1
else:
	if gpsfile_exists == True: #Plot Timestamp v LASTBEACONRSSI_distance when gps file is present
		fig,ax1 = plt.subplots()
		ax1.set_xlabel('Timestamp')
		ax1.set_ylabel('Stat Data', color= "black")
		lines, = ax1.plot(timestamplist5, LastBeaconRssiDataList, color="r" , marker = '+', markersize = 10)
		ax1.tick_params(axis='y', labelcolor="black")

		ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

		ax2.set_ylabel('Distance', color="b")  # we already handled the x-label with ax1
		liness, = ax2.plot(timestampgpslist, distancelist, color="b", marker = '+' , markersize = 10 , linestyle = ":")
		ax2.tick_params(axis='y', labelcolor="black")

		LastBeaconRssiDatalist_line = mlines.Line2D([], [], color='r', label='LastBeaconRssi Data', linestyle = ":")
		Distancelist_line = mlines.Line2D([], [], color='b', label='Distance', linestyle = ":")

		lgd = plt.legend(handles=[LastBeaconRssiDatalist_line,Distancelist_line],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		plt.title('Timestamp v LastBeaconRssi_Distance ',fontweight="bold")

	else:
		plt.figure(12)
		plt.ylabel('Stat Data')
		plt.title('Timestamp v LastBeaconRssi',fontweight="bold")
		plt.plot(timestamplist5, LastBeaconRssiDataList, marker = "+", linestyle = ":", color = "b")
		Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='lastbeaconrssi', linewidth = 0)
		lgd = plt.legend(handles=[Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))

if SKIPPLOT_LASTDATARSSI == 1:
	donothing = 1
else:
	if gpsfile_exists == True: #Plot Timestamp v LASTDATARSSI_distance when gps file is present
		fig,ax1 = plt.subplots()
		ax1.set_xlabel('Timestamp')
		ax1.set_ylabel('Stat Data', color= "black")
		lines, = ax1.plot(timestamplist5, LastDataRssiDataList, color="r" , marker = '+', markersize = 10)
		ax1.tick_params(axis='y', labelcolor="black")

		ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

		ax2.set_ylabel('Distance', color="b")  # we already handled the x-label with ax1
		liness, = ax2.plot(timestampgpslist, distancelist, color="b", marker = '+' , markersize = 10 , linestyle = ":")
		ax2.tick_params(axis='y', labelcolor="black")

		LastDataRssiDatalist_line = mlines.Line2D([], [], color='r', label='LastBeaconRssi Data', linestyle = ":")
		Distancelist_line = mlines.Line2D([], [], color='b', label='Distance', linestyle = ":")

		lgd = plt.legend(handles=[LastDataRssiDatalist_line,Distancelist_line],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		plt.title('Timestamp v LastBeaconRssi_Distance ',fontweight="bold")

	else:
		plt.figure(13)
		plt.ylabel('Stat Data')
		plt.title('Timestamp v LastDataRssi',fontweight="bold")
		plt.plot(timestamplist5, LastDataRssiDataList, marker = "+", linestyle = ":", color = "b")
		Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='lastdatarssi', linewidth = 0)
		lgd = plt.legend(handles=[Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))

if SKIPPLOT_CURRENTMCS == 1:
	donothing = 1
else:
	if gpsfile_exists == True: #Plot Timestamp v CURRENTMCS_distance when gps file is present
		fig,ax1 = plt.subplots()
		ax1.set_xlabel('Timestamp')
		ax1.set_ylabel('Stat Data', color= "black")
		lines, = ax1.plot(timestamplist5, CurrentMcsDataList, color="r" , marker = '+', markersize = 10)
		ax1.tick_params(axis='y', labelcolor="black")

		ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

		ax2.set_ylabel('Distance', color="b")  # we already handled the x-label with ax1
		liness, = ax2.plot(timestampgpslist, distancelist, color="b", marker = '+' , markersize = 10 , linestyle = ":")
		ax2.tick_params(axis='y', labelcolor="black")

		CurrentMcsDatalist_line = mlines.Line2D([], [], color='r', label='CurrentMcs Data', linestyle = ":")
		Distancelist_line = mlines.Line2D([], [], color='b', label='Distance', linestyle = ":")

		lgd = plt.legend(handles=[CurrentMcsDatalist_line,Distancelist_line],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		plt.title('Timestamp v CurrentMcs_Distance ',fontweight="bold")

	else:
		plt.figure(14)
		plt.ylabel('Stat Data')
		plt.title('Timestamp v CurrentMcs',fontweight="bold")
		plt.plot(timestamplist5, CurrentMcsDataList, marker = "+", linestyle = ":", color = "b")
		Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='currentmcs', linewidth = 0)
		lgd = plt.legend(handles=[Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))

if SKIPPLOT_RFTEMP == 1:
	donothing = 1
else:
	if gpsfile_exists == True: #Plot Timestamp v RFTEMP_distance when gps file is present
		fig,ax1 = plt.subplots()
		ax1.set_xlabel('Timestamp')
		ax1.set_ylabel('Stat Data', color= "black")
		lines, = ax1.plot(timestamplist5, RFTempDataList, color="r" , marker = '+', markersize = 10)
		ax1.tick_params(axis='y', labelcolor="black")

		ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

		ax2.set_ylabel('Distance', color="b")  # we already handled the x-label with ax1
		liness, = ax2.plot(timestampgpslist, distancelist, color="b", marker = '+' , markersize = 10 , linestyle = ":")
		ax2.tick_params(axis='y', labelcolor="black")

		RFTempDatalist_line = mlines.Line2D([], [], color='r', label='RFTemp Data', linestyle = ":")
		Distancelist_line = mlines.Line2D([], [], color='b', label='Distance', linestyle = ":")

		lgd = plt.legend(handles=[RFTempDatalist_line,Distancelist_line],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		plt.title('Timestamp v RFTemp_Distance ',fontweight="bold")

	else:
		plt.figure(15)
		plt.ylabel('Stat Data')
		plt.title('Timestamp v RFTempData',fontweight="bold")
		plt.plot(timestamplist5, RFTempDataList, marker = "+", linestyle = ":", color = "b")
		Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='rftempdata', linewidth = 0)
		lgd = plt.legend(handles=[Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))

if SKIPPLOT_BBTEMP == 1:
	donothing = 1
else:
	if gpsfile_exists == True: #Plot Timestamp v BBTEMP_distance when gps file is present
		fig,ax1 = plt.subplots()
		ax1.set_xlabel('Timestamp')
		ax1.set_ylabel('Stat Data', color= "black")
		lines, = ax1.plot(timestamplist5, BBTempDataList, color="r" , marker = '+', markersize = 10)
		ax1.tick_params(axis='y', labelcolor="black")

		ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

		ax2.set_ylabel('Distance', color="b")  # we already handled the x-label with ax1
		liness, = ax2.plot(timestampgpslist, distancelist, color="b", marker = '+' , markersize = 10 , linestyle = ":")
		ax2.tick_params(axis='y', labelcolor="black")

		BBTempDatalist_line = mlines.Line2D([], [], color='r', label='RFTemp Data', linestyle = ":")
		Distancelist_line = mlines.Line2D([], [], color='b', label='Distance', linestyle = ":")

		lgd = plt.legend(handles=[BBTempDatalist_line,Distancelist_line],loc='upper center', bbox_to_anchor=(0.55,-0.1))
		plt.title('Timestamp v BBTemp_Distance ',fontweight="bold")

	else:
		plt.figure(16)
		plt.ylabel('Stat Data')
		plt.title('Timestamp v BBTempData',fontweight="bold")
		plt.plot(timestamplist5, BBTempDataList, marker = "+", linestyle = ":", color = "b")
		Blue_cross = mlines.Line2D( [], [], color='b' , marker='+', markersize=10, label='bbtempdata', linewidth = 0)
		lgd = plt.legend(handles=[Blue_cross],loc='upper center', bbox_to_anchor=(0.55,-0.1))

plt.show()


print "INFO: END PROCESSING INPUT FILES\n"