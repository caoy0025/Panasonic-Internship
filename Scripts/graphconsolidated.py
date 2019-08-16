import sys, math
import numpy as np
import matplotlib.pyplot as plt
import csv, itertools , xlwt ,operator
import pandas as pd
from collections import OrderedDict
import os
import matplotlib.lines as mlines
from os import listdir
from PIL import Image
import glob, os
import PIL
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def list_files1(directory, extension):
	return (f for f in listdir(directory) if f.endswith('.' + extension))

#Variables
OUTPUT_FOLDER = "Results/"
OUTPUT_FOLDER2 = "Graphs/"
OUTPUT_FOLDER3 = "Graphs/Consolidated graphs/"
xaxislist = []
xaxislist2= []

#First group list
AverageBestBeamSNRDatalist = []
AverageSNRDataDatalist = []
AverageRemoteSNRDataDatalist = []

#Second graph group list
AveragePingDatalist = []
AverageTcpDatalist = []
AverageUdpDatalist = []
FrequentCurrentMcsDatalist = []

#Third graph group list
AverageRFTempDatalist = []
AverageBBTempDatalist = []
FrequentTxSectorDataDatalist = []
FrequentRxSectorDataDatalist = []

#Fourth graph group list
AverageLastRemoteRssiDatalist = []
AverageLastBeaconRssiDatalist = []
AverageLastDataRssiDatalist = []
AverageRSSIDataDatalist = []

#Finding each MCS file in Results folder
results = []
listofMCSfiles = []
results2 = []


listofperfimages = []
listofsupimages = []
listofstatimages = []

keywordperf = ["perf_"]

# Get log file name and check if valid
if len(sys.argv) != 2:
	print( "Correct usage: python extractplot<ver>.py [dir]/[filename].csv")
	quit() # not valid so exit

inputsummaryfiledir = sys.argv[1]

inputsummaryfiledir3 = inputsummaryfiledir + "/Consolidated files"



inputsummaryfiledir2 = inputsummaryfiledir + "/Graphs"
print(inputsummaryfiledir2)


results += [each for each in os.listdir(inputsummaryfiledir3) if each.endswith('.csv')]

results2 += [each for each in os.listdir(inputsummaryfiledir2) if each.endswith('.png')]


for element in results:
	if "output_sortedmerged_supstatperf_" in element:
		listofMCSfiles = listofMCSfiles + [str(inputsummaryfiledir3+"/"+element)]


lengthoflistofMCSfiles = len(listofMCSfiles)

#Creates empty files
# statsupfile = open(outputextractstatsup, "w")
# statsupfile.close()
# statsupsortedfile = open(outputextractstatsupsorted, "w")
# statsupsortedfile.close()
# supsortedmergedfile = open(outputextractstatsupsortedmerged, "w")
# supsortedmergedfile.close()


#Titles for different MCS files, same data
SaveNameAverageBestBeamSNRData = "graph_by_datatype_beastbeamsnr"
SaveNameAverageSNRDataData  = "graph_by_datatype_average_snr"
SaveNameAverageRemoteSNRDataData = "graph_by_datatype_average_remotesnr"

#Second graph group
SaveNameAveragePingData = "graph_by_datatype_average_ping"
SaveNameAverageTcpData = "graph_by_datatype_average_tcp"
SaveNameAverageUdpData = "graph_by_datatype_average_udp"
SaveNameFrequentCurrentMcsData = "graph_by_datatype_frequent_currentmcs"

#Third graph group
SaveNameAverageRFTempData = "graph_by_datatype_average_rftemp"
SaveNameAverageBBTempData = "graph_by_datatypes_average_bbtemp"
SaveNameFrequentTxSectorDataData = "graph_by_datatype_frequent_txsector"
SaveNameFrequentRxSectorDataData = "graph_by_datatype_frequent_rxsector"

#Fourth graph group
SaveNameAverageLastRemoteRssiData = "graph_by_datatype_average_lastremoterssi"
SaveNameAverageLastBeaconRssiData = "graph_by_datatype_average_lastbeaconrssi"
SaveNameAverageLastDataRssiData = "graph_by_datatype_average_lastdatarssi"
SaveNameAverageRSSIDataData = "graph_by_datatype_average_rssi"


#Creates empty string
SaveNameAverageBestBeamSNRDataMCSnumbers = ""
SaveNameAverageSNRDataDataMCSnumbers = ""
SaveNameAverageRemoteSNRDataDataMCSnumbers =  ""
SaveNameAveragePingDataMCSnumbers = ""
SaveNameAverageTcpDataMCSnumbers = ""
SaveNameAverageUdpDataMCSnumbers = "" 
SaveNameFrequentCurrentMcsDataMCSnumbers = ""
SaveNameAverageRFTempDataMCSnumbers = ""
SaveNameAverageBBTempDataMCSnumbers = ""
SaveNameFrequentTxSectorDataDataMCSnumbers = ""
SaveNameFrequentRxSectorDataDataMCSnumbers = ""
SaveNameAverageLastRemoteRssiDataMCSnumbers = "" 
SaveNameAverageLastBeaconRssiDataMCSnumbers = ""
SaveNameAverageLastDataRssiDataMCSnumbers = ""
SaveNameAverageRSSIDataDataMCSnumbers = ""


#Creating a list of lists for each data
# AverageBestBeamSNRDataMegalist = [[] for i in range(lengthoflistofMCSfiles )]
# AverageSNRDataDataMegalist = [[] for i in range(lengthoflistofMCSfiles )]
# AverageRemoteSNRDataDataMegalist =  [[] for i in range(lengthoflistofMCSfiles )]


# AveragePingDataMegalist = [[] for i in range(lengthoflistofMCSfiles )]
# AverageTcpDataMegalist = [[] for i in range(lengthoflistofMCSfiles )]
# AverageUdpDataMegalist = [[] for i in range(lengthoflistofMCSfiles )]
# FrequentCurrentMcsDataMegalist = [[] for i in range(lengthoflistofMCSfiles )]


# AverageRFTempDataMegalist = [[] for i in range(lengthoflistofMCSfiles )]
# AverageBBTempDataMegalist = [[] for i in range(lengthoflistofMCSfiles )]
# FrequentTxSectorDataDataMegalist = [[] for i in range(lengthoflistofMCSfiles )]
# FrequentRxSectorDataDataMegalist = [[] for i in range(lengthoflistofMCSfiles )]


# AverageLastRemoteRssiDataMegalist = [[] for i in range(lengthoflistofMCSfiles )]
# AverageLastBeaconRssiDataMegalist = [[] for i in range(lengthoflistofMCSfiles )]
# AverageLastDataRssiDataMegalist = [[] for i in range(lengthoflistofMCSfiles )]
# AverageRSSIDataDataMegalist = [[] for i in range(lengthoflistofMCSfiles )]			




for fileindex in range(lengthoflistofMCSfiles):

	with open(listofMCSfiles[fileindex], "rt") as inputsummary: #Input main file name
		

		nameoffile = str(listofMCSfiles[fileindex]).split('/')[4]
		nameoffile = nameoffile.split('_',3)
		nameoffile = nameoffile[3]

		longername = nameoffile.split(".")[0]

		#formates the original text title to get just the log file data
		tempname = "log_2"+longername.split("log_2")[-1]
		tempname = tempname.split("_mcs")[0]

		outputfilemcsnumber = str(listofMCSfiles[fileindex]).split("_")[-1]
		outputfilemcsnumber = outputfilemcsnumber.split('.')[0]


	

		inputsummarycontent = inputsummary.readlines()[1:]
		for line in inputsummarycontent:
			

			xaxis = line.split(",")[0] #find x axis
			
			#First graph group
			AverageBestBeamSNRData = line.split(",")[1]
			AverageSNRDataData = line.split(",")[13]
			AverageRemoteSNRDataData = line.split(",")[14]

			#Second graph group
			AveragePingData = line.split(",")[8]
			AverageTcpData = line.split(",")[10]
			AverageUdpData = line.split(",")[9]
			FrequentCurrentMcsData = line.split(",")[5]

			#Third graph group
			AverageRFTempData = line.split(",")[6]
			AverageBBTempData = line.split(",")[7]	
			FrequentTxSectorDataData = line.split(",")[11]
			FrequentRxSectorDataData = line.split(",")[12]

			#Fourth graph group
			AverageLastRemoteRssiData = line.split(",")[2]
			AverageLastBeaconRssiData = line.split(",")[3]
			AverageLastDataRssiData = line.split(",")[4]
			AverageRSSIDataData = line.split(",")[15]
			AverageRSSIDataData = AverageRSSIDataData.rstrip()

			xaxislist = xaxislist + [xaxis]


			#First graph group list
			AverageBestBeamSNRDatalist = AverageBestBeamSNRDatalist + [AverageBestBeamSNRData]
			AverageSNRDataDatalist = AverageSNRDataDatalist + [AverageSNRDataData]
			AverageRemoteSNRDataDatalist = AverageRemoteSNRDataDatalist + [AverageRemoteSNRDataData]

			#Second graph group list
			AveragePingDatalist = AveragePingDatalist + [AveragePingData]
			AverageTcpDatalist = AverageTcpDatalist + [AverageTcpData]
			AverageUdpDatalist = AverageUdpDatalist + [AverageUdpData]
			FrequentCurrentMcsDatalist = FrequentCurrentMcsDatalist + [FrequentCurrentMcsData]

			#Third graph group list
			AverageRFTempDatalist = AverageRFTempDatalist + [AverageRFTempData]
			AverageBBTempDatalist = AverageBBTempDatalist + [AverageBBTempData]
			FrequentTxSectorDataDatalist = FrequentTxSectorDataDatalist + [FrequentTxSectorDataData]
			FrequentRxSectorDataDatalist = FrequentRxSectorDataDatalist + [FrequentRxSectorDataData]

			#Fourth graph group list
			AverageLastRemoteRssiDatalist = AverageLastRemoteRssiDatalist + [AverageLastRemoteRssiData]
			AverageLastBeaconRssiDatalist = AverageLastBeaconRssiDatalist + [AverageLastBeaconRssiData]
			AverageLastDataRssiDatalist = AverageLastDataRssiDatalist + [AverageLastDataRssiData]
			AverageRSSIDataDatalist = AverageRSSIDataDatalist + [AverageRSSIDataData]



########################################## Creating mega lists #######################################################################

			# AverageBestBeamSNRDataMegalist[fileindex].insert(0,AverageBestBeamSNRData)
			# AverageSNRDataDataMegalist[fileindex].insert(0,AverageSNRDataData)
			# AverageRemoteSNRDataDataMegalist[fileindex].insert(0,AverageRemoteSNRDataData)


			# AveragePingDataMegalist[fileindex].insert(0,AveragePingData)
			# AverageTcpDataMegalist[fileindex].insert(0,AverageTcpData)
			# AverageUdpDataMegalist[fileindex].insert(0,AverageUdpData)
			# FrequentCurrentMcsDataMegalist[fileindex].insert(0,FrequentCurrentMcsData)


			# AverageRFTempDataMegalist[fileindex].insert(0,AverageRFTempData)
			# AverageBBTempDataMegalist[fileindex].insert(0,AverageBBTempData)
			# FrequentTxSectorDataDataMegalist[fileindex].insert(0,FrequentTxSectorDataData)
			# FrequentRxSectorDataDataMegalist[fileindex].insert(0,FrequentRxSectorDataData)


			# AverageLastRemoteRssiDataMegalist[fileindex].insert(0,AverageLastRemoteRssiData)
			# AverageLastBeaconRssiDataMegalist[fileindex].insert(0,AverageLastBeaconRssiData)
			# AverageLastDataRssiDataMegalist[fileindex].insert(0,AverageLastDataRssiData)
			# AverageRSSIDataDataMegalist[fileindex].insert(0,AverageRSSIDataData)

	

#######################################################################################################################################
		
	xaxislist = list(map(float,xaxislist))
	AverageBestBeamSNRDatalist = list(map(float,AverageBestBeamSNRDatalist))
	AverageSNRDataDatalist = list(map(float,AverageSNRDataDatalist))
	AverageRemoteSNRDataDatalist = list(map(float,AverageRemoteSNRDataDatalist))
	AveragePingDatalist = list(map(float,AveragePingDatalist))
	AverageTcpDatalist = list(map(float,AverageTcpDatalist))
	AverageUdpDatalist = list(map(float,AverageUdpDatalist))
	FrequentCurrentMcsDatalist = list(map(float,FrequentCurrentMcsDatalist))
	AverageRFTempDatalist = list(map(float,AverageRFTempDatalist))
	AverageBBTempDatalist = list(map(float,AverageBBTempDatalist))
	FrequentTxSectorDataDatalist = list(map(float,FrequentTxSectorDataDatalist))
	FrequentRxSectorDataDatalist = list(map(float,FrequentRxSectorDataDatalist))
	AverageLastRemoteRssiDatalist = list(map(float,AverageLastRemoteRssiDatalist))
	AverageLastBeaconRssiDatalist = list(map(float,AverageLastBeaconRssiDatalist))
	AverageLastDataRssiDatalist = list(map(float,AverageLastDataRssiDatalist))
	AverageRSSIDataDatalist = list(map(float,AverageRSSIDataDatalist))
	
	inputsummary.close()

	#Ploting graphs

	fig, ax1 = plt.subplots()
	ax1.set_xlabel('Distance')
	ax1.set_ylabel('Bandwidth', color= "black")
	lines, = ax1.plot(xaxislist, AverageUdpDatalist, color="r" , marker = 'o', markersize = 3.5)
	ax1.plot(xaxislist, AverageTcpDatalist, color="g", marker = 'o' , markersize = 3.5)
	ax1.tick_params(axis='y', labelcolor="black")

	ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

	ax2.set_ylabel('Ping / MCS data', color="black")  # we already handled the x-label with ax1
	liness, = ax2.plot(xaxislist, AveragePingDatalist, color="b", marker = '^' , markersize = 3.5 , linestyle = ":")
	ax2.plot(xaxislist, FrequentCurrentMcsDatalist, color="orange", marker = '^' , markersize = 3.5, linestyle = ":")
	ax2.tick_params(axis='y', labelcolor="black")

	AverageUdpDatalist_line = mlines.Line2D([], [], color='r', label='AverageUdpData')
	AverageTcpDatalist_line = mlines.Line2D([], [], color='g', label='AverageTcpData')
	AveragePingDatalist_line = mlines.Line2D([], [], color='b', label='AveragePingData' , linestyle = ":")
	FrequentCurrentMcsDatalist_line = mlines.Line2D([], [], color='orange', label='FrequentCurrentMcsData', linestyle = ":")

	lgd = plt.legend(handles=[AverageUdpDatalist_line,AverageTcpDatalist_line,AveragePingDatalist_line,FrequentCurrentMcsDatalist_line],loc='upper center', bbox_to_anchor=(0.55,-0.1))
	plt.title('Bandwidth_Ping_MCS Data vs Distance')
	plt.savefig(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graph_by_mcs_udp_tcp_ping_mcs_ " + longername + ".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

	test1 = inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graph_by_mcs_udp_tcp_ping_mcs_ " + longername + ".png"




	fig, ax3 = plt.subplots()
	ax3.set_xlabel('Distance')
	ax3.set_ylabel('Sector Data', color= "black")
	ax3.plot(xaxislist, FrequentTxSectorDataDatalist, color="r" , marker = 'o', markersize = 3.5)
	ax3.plot(xaxislist, FrequentRxSectorDataDatalist, color="g", marker = 'o' , markersize = 3.5)
	ax3.tick_params(axis='y', labelcolor="black")

	ax4 = ax3.twinx()  # instantiate a second axes that shares the same x-axis

	ax4.set_ylabel('Temp', color="black")  # we already handled the x-label with ax1
	ax4.plot(xaxislist, AverageBBTempDatalist, color="b", marker = '^' , markersize = 3.5, linestyle = ":")
	ax4.plot(xaxislist, AverageRFTempDatalist, color="orange", marker = '^' , markersize = 3.5, linestyle = ":")
	ax4.tick_params(axis='y', labelcolor="black")

	FrequentTxSectorDataDatalist_line = mlines.Line2D([], [], color='r', label='FrequentTxSectorData')
	FrequentRxSectorDataDatalist_line = mlines.Line2D([], [], color='g', label='FrequentRxSectorData')
	AverageBBTempDatalist_line = mlines.Line2D([], [], color='b', label='AverageBBTempData', linestyle = ":")
	AverageRFTempDatalist_line = mlines.Line2D([], [], color='orange', label='AverageRFTempData', linestyle = ":")

	lgd = plt.legend(handles=[FrequentTxSectorDataDatalist_line,FrequentRxSectorDataDatalist_line,AverageBBTempDatalist_line,AverageRFTempDatalist_line],loc='upper center', bbox_to_anchor=(0.55,-0.1))
	plt.title('Temp_Sector Data vs Distance')
	plt.savefig(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graph_by_mcs_txsector_rxsector_bbtemp_rftemp_" + longername + ".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

	test2 = inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graph_by_mcs_txsector_rxsector_bbtemp_rftemp_" + longername + ".png"


	fig, ax5 = plt.subplots()
	ax5.set_xlabel('Distance')
	ax5.set_ylabel('RSSI Data', color= "black")
	ax5.plot(xaxislist, AverageRSSIDataDatalist, color="r" , marker = 'o', markersize = 3.5)
	ax5.plot(xaxislist, AverageLastDataRssiDatalist, color="g", marker = 'o' , markersize = 3.5)
	ax5.plot(xaxislist, AverageLastBeaconRssiDatalist, color="b", marker = 'o' , markersize = 3.5)
	ax5.plot(xaxislist, AverageLastRemoteRssiDatalist, color="orange", marker = 'o' , markersize = 3.5)
	ax5.tick_params(axis='y', labelcolor="black")

	AverageRSSIDataDatalist_line = mlines.Line2D([], [], color='r', label='AverageRSSIDataData')
	AverageLastDataRssiDatalist_line = mlines.Line2D([], [], color='g', label='AverageLastDataRssiData')
	AverageLastBeaconRssiDatalist_line = mlines.Line2D([], [], color='b', label='AverageLastBeaconRssiData')
	AverageLastRemoteRssiDatalist_line = mlines.Line2D([], [], color='orange', label='AverageLastRemoteRssiData')

	lgd = plt.legend(handles=[AverageRSSIDataDatalist_line,AverageLastDataRssiDatalist_line,AverageLastBeaconRssiDatalist_line,AverageLastRemoteRssiDatalist_line],loc='upper center', bbox_to_anchor=(0.55,-0.1))
	plt.title('RSSI Data vs Distance')
	plt.savefig(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graph_by_mcs_rssi_lastrssi_beaconrssi_lastremoterssi_" + longername + ".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

	test3 = inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graph_by_mcs_rssi_lastrssi_beaconrssi_lastremoterssi_" + longername + ".png"

	fig, ax6 = plt.subplots()
	ax6.set_xlabel('Distance')
	ax6.set_ylabel('SNR Data', color= "black")
	ax6.plot(xaxislist, AverageSNRDataDatalist, color="r" , marker = 'o', markersize = 3.5)
	ax6.plot(xaxislist, AverageRemoteSNRDataDatalist, color="g", marker = 'o' , markersize = 3.5)
	ax6.plot(xaxislist, AverageBestBeamSNRDatalist, color="b", marker = 'o' , markersize = 3.5)
	ax6.tick_params(axis='y', labelcolor="black")

	AverageSNRDataDatalist_line = mlines.Line2D([], [], color='r', label='AverageSNRDataData')
	AverageRemoteSNRDataDatalist_line = mlines.Line2D([], [], color='g', label='AverageRemoteSNRDataData')
	AverageBestBeamSNRDatalist_line = mlines.Line2D([], [], color='b', label='AverageBestBeamSNRData')

	lgd = plt.legend(handles=[AverageSNRDataDatalist_line,AverageRemoteSNRDataDatalist_line,AverageBestBeamSNRDatalist_line],loc='upper center', bbox_to_anchor=(0.55,-0.1))
	plt.title('SNR Data vs Distance')
	plt.savefig(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graph_by_mcs_snr_remotesnr_bestbeamsnr_" + longername + ".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

	test4 = inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graph_by_mcs_snr_remotesnr_bestbeamsnr_" + longername + ".png"

	
	fig.tight_layout()  # otherwise the right y-label is slightly clipped


############################### Combining All MCS data grpahs into 1 pdf ###################################
 ##REFERENCE####
	# images = map(Image.open, [test1, test2, test3, test4])
	# widths, heights = zip(*(i.size for i in images))

	# total_width = sum(widths)
	# max_height = max(heights)

	# new_im = Image.new('RGB', (total_width, max_height))

	# x_offset = 0
	# for im in images:
	# 	new_im.paste(im, (x_offset,0))
	# 	x_offset += im.size[0]

	# new_im.save(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graphs_by_mcs" +"_" +nameoffile + ".png")
		
################################################################################################################################


	plt.figure(5)
	plt.plot(xaxislist, AverageBestBeamSNRDatalist, marker = 'o' , markersize = 3.5,label = str(outputfilemcsnumber))
	SaveNameAverageBestBeamSNRDataMCSnumbers = SaveNameAverageBestBeamSNRDataMCSnumbers +  "_" + outputfilemcsnumber # Creates a string of accumated MCS for each data type

	plt.figure(6)
	plt.plot(xaxislist, AverageSNRDataDatalist, marker = 'o' , markersize = 3.5,label = str(outputfilemcsnumber))
	SaveNameAverageSNRDataDataMCSnumbers = SaveNameAverageSNRDataDataMCSnumbers + "_" + outputfilemcsnumber

	plt.figure(7)
	plt.plot(xaxislist, AverageRemoteSNRDataDatalist, marker = 'o' , markersize = 3.5,label = str(outputfilemcsnumber))
	SaveNameAverageRemoteSNRDataDataMCSnumbers = SaveNameAverageRemoteSNRDataDataMCSnumbers + "_" + outputfilemcsnumber

	plt.figure(8)
	plt.plot(xaxislist, AveragePingDatalist, marker = 'o' , markersize = 3.5,label = str(outputfilemcsnumber))
	SaveNameAveragePingDataMCSnumbers = SaveNameAveragePingDataMCSnumbers + "_" + outputfilemcsnumber

	plt.figure(9)
	plt.plot(xaxislist, AverageTcpDatalist, marker = 'o' , markersize = 3.5,label = str(outputfilemcsnumber))
	SaveNameAverageTcpDataMCSnumbers = SaveNameAverageTcpDataMCSnumbers + "_" + outputfilemcsnumber

	plt.figure(10)
	plt.plot(xaxislist, AverageUdpDatalist, marker = 'o' , markersize = 3.5,label = str(outputfilemcsnumber))
	SaveNameAverageUdpDataMCSnumbers = SaveNameAverageUdpDataMCSnumbers + "_" + outputfilemcsnumber

	plt.figure(11)
	plt.plot(xaxislist, FrequentCurrentMcsDatalist, marker = 'o' , markersize = 3.5,label = str(outputfilemcsnumber))
	SaveNameFrequentCurrentMcsDataMCSnumbers = SaveNameFrequentCurrentMcsDataMCSnumbers + "_" + outputfilemcsnumber

	plt.figure(12)
	plt.plot(xaxislist, AverageRFTempDatalist, marker = 'o' , markersize = 3.5,label = str(outputfilemcsnumber))
	SaveNameAverageRFTempDataMCSnumbers = SaveNameAverageRFTempDataMCSnumbers + "_" + outputfilemcsnumber

	plt.figure(13)
	plt.plot(xaxislist, AverageBBTempDatalist, marker = 'o' , markersize = 3.5,label = str(outputfilemcsnumber))
	SaveNameAverageBBTempDataMCSnumbers = SaveNameAverageBBTempDataMCSnumbers + "_" + outputfilemcsnumber

	plt.figure(14)
	plt.plot(xaxislist, FrequentTxSectorDataDatalist, marker = 'o' , markersize = 3.5,label = str(outputfilemcsnumber))
	SaveNameFrequentTxSectorDataDataMCSnumbers = SaveNameFrequentTxSectorDataDataMCSnumbers + "_" + outputfilemcsnumber

	plt.figure(15)
	plt.plot(xaxislist, FrequentRxSectorDataDatalist, marker = 'o' , markersize = 3.5,label = str(outputfilemcsnumber))
	SaveNameFrequentRxSectorDataDataMCSnumbers = SaveNameFrequentRxSectorDataDataMCSnumbers + "_" + outputfilemcsnumber

	plt.figure(16)
	plt.plot(xaxislist, AverageLastRemoteRssiDatalist, marker = 'o' , markersize = 3.5,label = str(outputfilemcsnumber))
	SaveNameAverageLastRemoteRssiDataMCSnumbers = SaveNameAverageLastRemoteRssiDataMCSnumbers + "_" + outputfilemcsnumber

	plt.figure(17)
	plt.plot(xaxislist, AverageLastBeaconRssiDatalist, marker = 'o' , markersize = 3.5,label = str(outputfilemcsnumber))
	SaveNameAverageLastBeaconRssiDataMCSnumbers = SaveNameAverageLastBeaconRssiDataMCSnumbers + "_" + outputfilemcsnumber

	plt.figure(18)
	plt.plot(xaxislist, AverageLastDataRssiDatalist, marker = 'o' , markersize = 3.5,label = str(outputfilemcsnumber))
	SaveNameAverageLastDataRssiDataMCSnumbers = SaveNameAverageLastDataRssiDataMCSnumbers + "_" + outputfilemcsnumber

	plt.figure(19)
	plt.plot(xaxislist, AverageRSSIDataDatalist, marker = 'o' , markersize = 3.5,label = str(outputfilemcsnumber))
	SaveNameAverageRSSIDataDataMCSnumbers = SaveNameAverageRSSIDataDataMCSnumbers +"_" + outputfilemcsnumber



	#Clearing lists 
	#First group list
	AverageBestBeamSNRDatalist = []
	AverageSNRDataDatalist = []
	AverageRemoteSNRDataDatalist = []

	#Second graph group list
	AveragePingDatalist = []
	AverageTcpDatalist = []
	AverageUdpDatalist = []
	FrequentCurrentMcsDatalist = []

	#Third graph group list
	AverageRFTempDatalist = []
	AverageBBTempDatalist = []
	FrequentTxSectorDataDatalist = []
	FrequentRxSectorDataDatalist = []

	#Fourth graph group list
	AverageLastRemoteRssiDatalist = []
	AverageLastBeaconRssiDatalist = []
	AverageLastDataRssiDatalist = []
	AverageRSSIDataDatalist = []

	xaxislist = []





plt.figure(5)
plt.xlabel('Distance')
plt.ylabel('BestBeamSNRData', color= "black")
plt.title('Average BestBeamSNRData vs Distance')
lgd = plt.legend(loc='upper left',bbox_to_anchor=(0.40,-0.1))
SaveNameAverageBestBeamSNRData = SaveNameAverageBestBeamSNRData + "_" + tempname +  str(SaveNameAverageBestBeamSNRDataMCSnumbers)
plt.savefig(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + SaveNameAverageBestBeamSNRData + ".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

plt.figure(6)
plt.xlabel('Distance')
plt.ylabel('AverageSNRData', color= "black")
plt.title('Average SNRData vs Distance')
lgd = plt.legend(loc='upper left',bbox_to_anchor=(0.40,-0.1))
SaveNameAverageSNRDataData = SaveNameAverageSNRDataData + "_" + tempname +  str(SaveNameAverageSNRDataDataMCSnumbers)
plt.savefig(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + SaveNameAverageSNRDataData + ".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

plt.figure(7)
plt.xlabel('Distance')
plt.ylabel('AverageRemoteSNRData', color= "black")
plt.title('Average RemoteSNRData vs Distance')
lgd = plt.legend(loc='upper left',bbox_to_anchor=(0.40,-0.1))
SaveNameAverageRemoteSNRDataData = SaveNameAverageRemoteSNRDataData + "_" + tempname + str(SaveNameAverageRemoteSNRDataDataMCSnumbers)
plt.savefig(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + SaveNameAverageRemoteSNRDataData + ".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

plt.figure(8)
plt.xlabel('Distance')
plt.ylabel('AveragePingData', color= "black")
plt.title('Average AveragePingData vs Distance')
lgd = plt.legend(loc='upper left',bbox_to_anchor=(0.40,-0.1))
SaveNameAveragePingData = SaveNameAveragePingData + "_" + tempname + str(SaveNameAveragePingDataMCSnumbers)
plt.savefig(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + SaveNameAveragePingData + ".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

plt.figure(9)
plt.xlabel('Distance')
plt.ylabel('AverageTcpData', color= "black")
plt.title('Average AverageTcpData vs Distance')
lgd = plt.legend(loc='upper left',bbox_to_anchor=(0.40,-0.1))
SaveNameAverageTcpData = SaveNameAverageTcpData + "_" + tempname + str(SaveNameAverageTcpDataMCSnumbers)
plt.savefig(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + SaveNameAverageTcpData + ".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

plt.figure(10)
plt.xlabel('Distance')
plt.ylabel('AverageUdpData', color= "black")
plt.title('Average AverageUdpData vs Distance')
lgd = plt.legend(loc='upper left',bbox_to_anchor=(0.40,-0.1))
SaveNameAverageUdpData = SaveNameAverageUdpData + "_" + tempname + str(SaveNameAverageUdpDataMCSnumbers)
plt.savefig(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + SaveNameAverageUdpData + ".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

plt.figure(11)
plt.xlabel('Distance')
plt.ylabel('CurrentMcsData', color= "black")
plt.title('Frequent CurrentMcsData vs Distance')
lgd = plt.legend(loc='upper left',bbox_to_anchor=(0.40,-0.1))
SaveNameFrequentCurrentMcsData = SaveNameFrequentCurrentMcsData + "_" + tempname + str(SaveNameFrequentCurrentMcsDataMCSnumbers)
plt.savefig(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + SaveNameFrequentCurrentMcsData + ".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

plt.figure(12)
plt.xlabel('Distance')
plt.ylabel('RFTempData', color= "black")
plt.title('Average RFTempData vs Distance')
lgd = plt.legend(loc='upper left',bbox_to_anchor=(0.40,-0.1))
SaveNameAverageRFTempData = SaveNameAverageRFTempData + "_" + tempname + str(SaveNameAverageRFTempDataMCSnumbers)
plt.savefig(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + SaveNameAverageRFTempData + ".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

plt.figure(13)
plt.xlabel('Distance')
plt.ylabel('BBTempData', color= "black")
plt.title('Average BBTempData vs Distance')
lgd = plt.legend(loc='upper left',bbox_to_anchor=(0.40,-0.1))
SaveNameAverageBBTempData = SaveNameAverageBBTempData + "_" + tempname + str(SaveNameAverageBBTempDataMCSnumbers)
plt.savefig(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + SaveNameAverageBBTempData + ".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

plt.figure(14)
plt.xlabel('Distance')
plt.ylabel('TxSectorData', color= "black")
plt.title('Frequent TxSectorData vs Distance')
lgd = plt.legend(loc='upper left',bbox_to_anchor=(0.40,-0.1))
SaveNameFrequentTxSectorDataData = SaveNameFrequentTxSectorDataData + "_" +  tempname + str(SaveNameFrequentTxSectorDataDataMCSnumbers)
plt.savefig(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + SaveNameFrequentTxSectorDataData + ".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

plt.figure(15)
plt.xlabel('Distance')
plt.ylabel('RxSectorData', color= "black")
plt.title('Frequent RxSectorData vs Distance')
lgd = plt.legend(loc='upper left',bbox_to_anchor=(0.40,-0.1))
SaveNameFrequentRxSectorDataData = SaveNameFrequentRxSectorDataData + "_" + tempname + str(SaveNameFrequentRxSectorDataDataMCSnumbers)
plt.savefig(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + SaveNameFrequentRxSectorDataData + ".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

plt.figure(16)
plt.xlabel('Distance')
plt.ylabel('LastRemoteRssiData', color= "black")
plt.title('Average LastRemoteRssiData vs Distance')
lgd = plt.legend(loc='upper left',bbox_to_anchor=(0.40,-0.1))
SaveNameAverageLastRemoteRssiData = SaveNameAverageLastRemoteRssiData + "_" + tempname + str(SaveNameAverageLastRemoteRssiDataMCSnumbers)
plt.savefig(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + SaveNameAverageLastRemoteRssiData+ ".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

plt.figure(17)
plt.xlabel('Distance')
plt.ylabel('LastBeaconRssiData', color= "black")
plt.title('Average LastBeaconRssiData vs Distance')
lgd = plt.legend(loc='upper left',bbox_to_anchor=(0.40,-0.1))
SaveNameAverageLastBeaconRssiData = SaveNameAverageLastBeaconRssiData + "_" + tempname + str(SaveNameAverageLastBeaconRssiDataMCSnumbers)
plt.savefig(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + SaveNameAverageLastBeaconRssiData + ".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

plt.figure(18)
plt.xlabel('Distance')
plt.ylabel('LastDataRssiData', color= "black")
plt.title('Average LastDataRssiData vs Distance')
lgd = plt.legend(loc='upper left',bbox_to_anchor=(0.40,-0.1))
SaveNameAverageLastDataRssiData = SaveNameAverageLastDataRssiData + "_" + tempname + str(SaveNameAverageLastDataRssiDataMCSnumbers)
plt.savefig(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + SaveNameAverageLastDataRssiData + ".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

plt.figure(19)
plt.xlabel('Distance')
plt.ylabel('RSSIData', color= "black")
plt.title('Average RSSIData vs Distance')
lgd = plt.legend(loc='upper left',bbox_to_anchor=(0.40,-0.1))
SaveNameAverageRSSIDataData = SaveNameAverageRSSIDataData + "_" + tempname + str(SaveNameAverageRSSIDataDataMCSnumbers)
plt.savefig(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + SaveNameAverageRSSIDataData + ".png", bbox_extra_artists=(lgd,), bbox_inches='tight')
#plt.show()




################################## Finding and consolidation of sup, perf, stat sup images ####################################


#mcs is in a list called findingmcs<>
findingthemcs=[]
findingthemcs2 = []
findingthemcs3 = []

for line in results2:
	# for word in keywordperf:
	if "perf_" in line:
		listofperfimages = listofperfimages + [line]
		mymcs = "mcs" + line.split("_mcs")[1][:-4]
		if mymcs not in findingthemcs:
			findingthemcs = findingthemcs + [mymcs]
	if "sup_" in line:
		listofsupimages = listofsupimages + [line]
		mymcs2 = "mcs" + line.split("_mcs")[1][:-4]
		if mymcs2 not in findingthemcs2:
			findingthemcs2 = findingthemcs2 + [mymcs2]

	if "stat_" in line:
		listofstatimages = listofstatimages + [line]
		mymcs3 = "mcs" + line.split("_mcs")[1][:-4]
		if mymcs3 not in findingthemcs3:
			findingthemcs3 = findingthemcs3 + [mymcs3]



findingthemcs = [x+"." for x in findingthemcs]
findingthemcs2 = [x+"." for x in findingthemcs2]
findingthemcs3 = [x+"." for x in findingthemcs3]
#print ("TEST")


#Folder of where the graphs are
xxx =  inputsummaryfiledir + str("/Graphs/") 


imagelist = []
imagelist2 = []
imagelist3 = []


findingthemcs = ['mcs1.', 'mcs9.', 'mcs12.', 'mcs-.', 'mcs4.']

#Matches mcs with elements of list containing png files
for elementmcs in findingthemcs:
	for elementperf in listofperfimages:
		if elementmcs in elementperf:
			imagelist = imagelist + [elementperf]
	

	imagelist = [str(xxx) + x for x in imagelist]

	images = list(map(Image.open, imagelist))
	widths, heights = zip(*(i.size for i in images))

	total_width = sum(widths)
	max_height = max(heights)

	new_im = Image.new('RGB', (total_width, max_height))

	x_offset = 0
	for im in images:
		new_im.paste(im, (x_offset,0))
		x_offset += im.size[0]

	#new_im.save(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graphs_by_mcs" +"_" +nameoffile + ".png")
	new_im.save(inputsummaryfiledir + "/" + OUTPUT_FOLDER3 + "graphs_summary_by_mcs_perf_" + elementmcs + "png")
	perffile = inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graphs_summary_by_mcs_perf_" + elementmcs + "png"
	imagelist = []


findingthemcs2 = ['mcs1.', 'mcs9.', 'mcs4.', 'mcs-.', 'mcs12.']

for elementmcs in findingthemcs2:
	for index, elementsup in enumerate(listofsupimages):
		if elementmcs in elementsup:
			imagelist2 = imagelist2 + [elementsup]

	imagelist2firsthalf = imagelist2[0:3]
	imagelist2secondhalf = imagelist2[3:]

	imagelist2firsthalf = [str(xxx) + x for x in imagelist2firsthalf]

	# Code to consolidate #

	images = list(map(Image.open, imagelist2firsthalf))
	widths, heights = zip(*(i.size for i in images))

	total_width = sum(widths)
	max_height = max(heights)

	new_im = Image.new('RGB', (total_width, max_height))


	x_offset = 0
	for im in images:
		new_im.paste(im, (x_offset,0))
		x_offset += im.size[0]

	#new_im.save(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graphs_by_mcs" +"_" +nameoffile + ".png")
	new_im.save(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graphs_summary_by_mcs_sup_part_1_" + elementmcs + "png")
	#new_im.show(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graphs_summary_by_mcs_sup_part_1_" + elementmcs + "png")



	summary1part1 = inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graphs_summary_by_mcs_sup_part_1_" + elementmcs + "png" #Used to consolidate 2 part summary graphs to be vertical

	imagelist2secondhalf = [str(xxx) + x for x in imagelist2secondhalf]
	#imagelist2secondhalf = imagelist2secondhalf + ["/home/caoyun/Work/Active/scripts/blank.png"]  #Added blank file to make the consolidated graphs to be proportional

	images = list(map(Image.open, imagelist2secondhalf))
	widths, heights = zip(*(i.size for i in images))

	total_width = sum(widths)
	max_height = max(heights)

	new_im = Image.new('RGB', (total_width, max_height))

	x_offset = 0
	for im in images:
		new_im.paste(im, (x_offset,0))
		x_offset += im.size[0]

	#new_im.save(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graphs_by_mcs" +"_" +nameoffile + ".png")
	
	new_im.save(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 +"graphs_summary_by_mcs_sup_part_2_" + elementmcs + "png")
	#new_im.show(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 +"graphs_summary_by_mcs_sup_part_2_" + elementmcs + "png")


	summary1part2 = inputsummaryfiledir + "/" + OUTPUT_FOLDER2 +"graphs_summary_by_mcs_sup_part_2_" + elementmcs + "png" #Used to consolidate 2 part summary graphs to be vertical

	imagelist2 = []
	imagelist2firsthalf = []
	imagelist2secondhalf = []

findingthemcs3 = ['mcs1.', 'mcs9.', 'mcs12.', 'mcs-.', 'mcs4.']
for elementmcs in findingthemcs3:
	for elementstat in listofstatimages:
		if elementmcs in elementstat:
			imagelist3 = imagelist3 + [elementstat]


	imagelist3firsthalf = imagelist3[0:4]
	imagelist3secondhalf = imagelist3[4:]



	imagelist3firsthalf = [str(xxx) + x for x in imagelist3firsthalf]

	images = list(map(Image.open, imagelist3firsthalf))
	widths, heights = zip(*(i.size for i in images))

	total_width = sum(widths)
	max_height = max(heights)

	new_im = Image.new('RGB', (total_width, max_height))

	x_offset = 0
	for im in images:
		new_im.paste(im, (x_offset,0))
		x_offset += im.size[0]

	#new_im.save(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graphs_by_mcs" +"_" +nameoffile + ".png")
	new_im.save(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graphs_summary_by_mcs_stat_part_1_" + elementmcs + "png")

	summary2part1 = inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graphs_summary_by_mcs_stat_part_1_" + elementmcs + "png" #Used to consolidate 2 part summary graphs to be vertical


	imagelist3secondhalf = [str(xxx) + x for x in imagelist3secondhalf]
	imagelist3secondhalf = imagelist3secondhalf + ["/home/caoyun/Work/Active/scripts/blank.png"] #Added blank file to make the consolidated graphs to be proportional
	
	images = list(map(Image.open, imagelist3secondhalf))
	widths, heights = list(zip(*(i.size for i in images)))

	total_width = sum(widths)
	max_height = max(heights)

	new_im = Image.new('RGB', (total_width, max_height))

	x_offset = 0
	for im in images:
		new_im.paste(im, (x_offset,0))
		x_offset += im.size[0]

	#new_im.save(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graphs_by_mcs" +"_" +nameoffile + ".png")
	new_im.save(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graph_summary_by_mcs_stat_part_2_" + elementmcs + "png")

	summary2part2 = inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graph_summary_by_mcs_stat_part_2_" + elementmcs + "png" #Used to consolidate 2 part summary graphs to be vertical

	imagelist3 = []
	imagelist3firsthalf = []
	imagelist3secondhalf = []

	################################# Consolidating vertically #################################################

	#Vertical consolidation for sup

	list_im = [summary1part1, summary1part2]
	imgs  = [ PIL.Image.open(i) for i in list_im ]
	# pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
	min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
	#max_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[len(imgs)-1][1]
	imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

	# for a vertical stacking it is simple: use vstack
	imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
	imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
	imgs_comb = PIL.Image.fromarray( imgs_comb)
	imgs_comb.save(inputsummaryfiledir + "/" + OUTPUT_FOLDER3 +"graphs_summary_by_mcs_sup_" + tempname + elementmcs + "png" )


	#Vertical consolidation for stat

	list_im = [summary2part1, summary2part2]
	imgs  = [ PIL.Image.open(i) for i in list_im ]
	# pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
	min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
	#mgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

	# for a vertical stacking it is simple: use vstack
	imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
	imgs_comb = PIL.Image.fromarray( imgs_comb)
	imgs_comb.save(inputsummaryfiledir + "/" + OUTPUT_FOLDER3 +"graph_summary_by_mcs_stat_" + tempname +  elementmcs + "png" )





	findingthemcs = []
	findingthemcs2 = []
	findingthemcs3 = []



# images = map(Image.open, [test1, test2, test3, test4])
# widths, heights = zip(*(i.size for i in images))

# total_width = sum(widths)
# max_height = max(heights)

# new_im = Image.new('RGB', (total_width, max_height))

# x_offset = 0
# for im in images:
# 	new_im.paste(im, (x_offset,0))
# 	x_offset += im.size[0]

# new_im.save(inputsummaryfiledir + "/" + OUTPUT_FOLDER2 + "graphs_by_mcs" +"_" +nameoffile + ".png")




print( "\nSummary:")
print( "Input:")
#print( outputextractsupstatsupperfsortedmerged
print( "Output:")
print( (inputsummaryfiledir + "/" + OUTPUT_FOLDER3 + "graphs_summary_by_mcs_perf_" + elementmcs + "png"))
print( (inputsummaryfiledir + "/" + OUTPUT_FOLDER3 +"graphs_summary_by_mcs_sup_" + tempname + elementmcs + "png" ))
print( (inputsummaryfiledir + "/" + OUTPUT_FOLDER3 +"graph_summary_by_mcs_stat_" + tempname +  elementmcs + "png" ))

try:
	os.remove(perffile)
except:
	donothing=1	
try:
	os.remove(summary1part1)
except:
	donothing=1	
try:
	os.remove(summary1part2)
except:
	donothing=1				
try:
	os.remove(summary2part1)
except:
	donothing=1
try:
	os.remove(summary2part2)
except:
	donothing=1								
