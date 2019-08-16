import csv, itertools , xlwt , sys , os
import time
from io import StringIO

from bisect import *
import datetime
import glob


# Lists
TxSectorDataList = []
# RxSectorDataList = []
# SNRDataList = []
# RemoteSNRDataList = []
# RSSIDataList = []
# udpbandwidthdatalist = []
# tcpbandwidthdatalist = []

# BestBeamSNRDataList = []
# LastRemoteRssiDataList = []
# LastBeaconRssiDataList = []
# LastDataRssiDataList = []
# CurrentMcsDataList = []
# RFTempDataList = []
# BBTempDataList = []
Timestamplist = []

udpchecktime = ""
tcpchecktime = ""
tcpchecktimeend = 0.0
udpchecktimeend = 0.0
prevudpchecktime = 0.0

def twos_comp(val, bits): #"""compute the 2's complement of int value val"""
	if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
		val = val - (1 << bits)        # compute negative value
	return val                         # return positive value as is


def hex_to_dex(strng_of_hex):
	return int(strng_of_hex, 16)

if len(sys.argv) != 2:
	print "Correct usage: python extractplot<ver>.py [dir]/[filename].csv"
	quit() # not valid so exit

inputlogfiledir = sys.argv[1]

#Finds the total number of tsmerge files in dir
tsmergerfileCounter = len(glob.glob1(inputlogfiledir,"output_tsmerge*.csv"))
filecount = 1




for file in os.listdir(inputlogfiledir):
	if "output_tsmerge" in file:
		
		filetoopen = file
		filename = filetoopen.split(".")[0]
		filename = str(filename) + "_summary.csv"


		with open(str(inputlogfiledir)+ "/Tsmergedata/" + filename, "wb") as resultfile:
			writer = csv.DictWriter(resultfile, fieldnames = ["Timestamp", "TxSectorData", "RxSectorData",  "SNRData", "RemoteSNRData" , "RSSIData" ,"UDP Bandwidth", "TCP Bandwidth", "BestBeamSNR", "LastRemoteRssi",  "LastBeaconRssi", "LastDataRssi" , "CurrentMcs" , "RFTemp", "BBTemp"], delimiter = ',' )
			writer.writeheader()

			udpchecktime = ""
			tcpchecktime = ""
			tcpchecktimeend = 0.0
			udpchecktimeend = 0.0
		
			with open (str(inputlogfiledir)+ "/" +  filetoopen, 'rU') as file1:
				tsmergefile = file1.read().splitlines()[1:] #read scond line onwards
				
				#print "Start first main loop"

				for line in tsmergefile:
			
					timestamp = line.split(",")[0]
					supdataline = line.split(",")[1]
					udpdataline = line.split(",")[2]
					tcppdataline = line.split(",")[3]
					statdataline = line.split(",")[4]


					
					TxSectorData=""
					RxSectorData = ""
					SNRData = ""
					RemoteSNRData = ""
					RSSIData = ""
					udpbandwidth = "" 
					tcpbandwidth = ""

					BestBeamSNRData = ""
					LastRemoteRssiData = ""
					LastBeaconRssiData = ""
					LastDataRssiData = ""
					CurrentMcsData = ""
					RFTempData = ""
					BBTempData = ""


					# Finding sup data
					if "BF-EVENT-DATA" in supdataline:

						supdata = supdataline.split(" ")[1]
					
						TxSectorData = supdata.split(';')[0]
					 	#TxSectorDataList = TxSectorDataList + [TxSectorData]

						
					 	RxSectorData = supdata.split(';')[1]
					 	#RxSectorDataList = RxSectorDataList + [RxSectorData]
						
					 	SNRData = supdata.split(';')[2]
						#TotalSNR = TotalSNR + float(SNRData)
					 	#SNRDataList = SNRDataList + [SNRData]
						
					 	RemoteSNRData = supdata.split(';')[3]
						#TotalRemoteSNR = TotalRemoteSNR + float(RemoteSNRData)
					 	#RemoteSNRDataList = RemoteSNRDataList + [RemoteSNRData]

					 	RSSIData = supdata.split(';')[4]
						#TotalRSSI = TotalRSSI + float(RSSIData)
					 	#RSSIDataList = RSSIDataList + [RSSIData]
					 
					# Finding udp data
					if  "Mbits/sec" in udpdataline: 
						udpdata = line.rsplit(",",2)[0]
						udpdata = udpdata.split(",",2)[2]
						udpbandwidth = udpdata.split("Mbits/sec")[0]
						udpbandwidth = udpbandwidth.rsplit(" ",2)[1]
						udpbandwidth = udpbandwidth.strip()

						udpchecktimeline = udpdata.split("sec")[0]
						udpchecktimebeginningline = udpchecktimeline.split("-")[0]
						udpchecktimebeginning = udpchecktimebeginningline.rsplit(" ")[-1]


						if float(udpchecktimeend) > float(udpchecktimebeginning):
							continue
						udpchecktimeend = udpchecktimeline.rsplit("-")[-1]

						udpchecktime = float(udpchecktimeend) - float(udpchecktimebeginning)

		
						
	

						#udpbandwidthdatalist = udpbandwidthdatalist + [udpbandwidth]
					elif "Gbits/sec" in udpdataline:
						udpdata = line.rsplit(",",2)[0]
						udpdata = udpdata.split(",",2)[2]
						udpbandwidth = udpdata.split("Gbits/sec")[0]
						udpbandwidth = udpbandwidth.rsplit(" ",2)[1]
						udpbandwidth = udpbandwidth.strip()
						udpbandwidth = float(udpbandwidth) * 1000

						udpchecktimeline = udpdata.split("sec")[0]
						udpchecktimebeginningline = udpchecktimeline.split("-")[0]
						udpchecktimebeginning = udpchecktimebeginningline.rsplit(" ")[-1]


						if float(udpchecktimeend) > float(udpchecktimebeginning):
							continue
						udpchecktimeend = udpchecktimeline.rsplit("-")[-1]

						udpchecktime = float(udpchecktimeend) - float(udpchecktimebeginning)

					
						

					# Finding Tcp data
					if "Mbits/sec" in tcppdataline:
						tcpdata = line.split(",",3)[3]
						tcpdata = tcpdata.rsplit(",",1)[0]
						tcpbandwidth = tcpdata.split("Mbits/sec")[0]
						tcpbandwidth = tcpbandwidth.rsplit(" ",2)[1]
						tcpbandwidth = tcpbandwidth.strip()
						

						tcpchecktimeline = tcpdata.split("sec")[0]
						tcpchecktimebeginningline = tcpchecktimeline.split("-")[0]
						tcpchecktimebeginning = tcpchecktimebeginningline.rsplit(" ")[-1]


						if float(tcpchecktimeend) > float(tcpchecktimebeginning):
							continue						
						tcpchecktimeend = tcpchecktimeline.rsplit("-")[-1]

						tcpchecktime = float(tcpchecktimeend) - float(tcpchecktimebeginning)

				

					elif "Gbits/sec" in tcppdataline:
						tcpdata = line.split(",",3)[3]
						tcpdata = tcpdata.rsplit(",",1)[0]
						tcpbandwidth = tcpdata.split("Mbits/sec")[0]
						tcpbandwidth = tcpbandwidth.rsplit(" ",2)[1]
						tcpbandwidth = tcpbandwidth.strip()
						tcpbandwidth = float(tcpbandwidth) * 1000


						tcpchecktimeline = tcpdata.split("sec")[0]	
						tcpchecktimebeginningline = tcpchecktimeline.split("-")[0]
						tcpchecktimebeginning = tcpchecktimebeginningline.rsplit(" ")[-1]

						if float(tcpchecktimeend) > float(tcpchecktimebeginning):
							continue	
					
						tcpchecktimeend = tcpchecktimeline.rsplit("-")[-1]

						tcpchecktime = float(tcpchecktimeend) - float(tcpchecktimebeginning)

						#tcpbandwidthdatalist = tcpbandwidthdatalist + [tcpbandwidth]

					# Finding Stat data
					if "STATS-EVENT-DATA:" in statdataline:

						statdata = statdataline.split(" ")[1]

						BestBeamSNRData = statdata.split(';')[0]
						# BestBeamSNRDataList = BestBeamSNRDataList + [BestBeamSNRData]
						# TotalBestBeamSNR = TotalBestBeamSNR + float(BestBeamSNRData)

						LastRemoteRssiData = statdata.split(';')[1]
						# LastRemoteRssiDataList = LastRemoteRssiDataList + [LastRemoteRssiData]
						# TotalLastRemoteRssi = TotalLastRemoteRssi + float(LastRemoteRssiData)

						LastBeaconRssiData = statdata.split(';')[2]
						# LastBeaconRssiDataList = LastBeaconRssiDataList + [LastBeaconRssiData]
						# TotalLastBeaconRssi = TotalLastBeaconRssi + float(LastBeaconRssiData)

						LastDataRssiData = statdata.split(';')[3]
						# LastDataRssiDataList = LastDataRssiDataList + [LastDataRssiData]
						# TotalLastDataRssi = TotalLastDataRssi + float(LastDataRssiData)

						CurrentMcsData = statdata.split(';')[4]
						#CurrentMcsDataList = CurrentMcsDataList + [CurrentMcsData]


						RFTempData = statdata.split(';')[5]
						# RFTempDataList = RFTempDataList + [RFTempData]
						# TotalRFTemp = TotalRFTemp + float(RFTempData)
					

						BBTempData = statdata.split(';')[6]
						# BBTempDataList = BBTempDataList + [BBTempData]
						# TotalBBTemp = TotalBBTemp + float(BBTempData)
					
					elif "FAIL" in statdataline:

						BestBeamSNRData = "FAIL"

						LastRemoteRssiData = "FAIL"

						LastBeaconRssiData = "FAIL"

						LastDataRssiData = "FAIL"

						CurrentMcsData = "FAIL"

						RFTempData = "FAIL"
					
						BBTempData = "FAIL"

					alldata =  str(timestamp) + "," + str(TxSectorData) + "," + str(RxSectorData) + "," + str(SNRData) + "," + str(RemoteSNRData) + "," + str(RSSIData) + "," + str(udpbandwidth) + "," + str(tcpbandwidth) + "," + str(BestBeamSNRData) + "," + str(LastRemoteRssiData) + "," + str(LastBeaconRssiData) + "," + str(LastDataRssiData) + "," + str(CurrentMcsData) + "," + str(RFTempData) + "," + str(BBTempData) + "\n"
					resultfile.write(alldata)
				#print "End 1st Main loop"
			resultfile.close()		

	######## Finding group data by data type ################ 
	#Open summary and make data type files
		with open (str(inputlogfiledir) +"/Tsmergedata/" + filename) as groupinfile:

		 	next(groupinfile) # Skips header
		 	
		 	UdpLineList = []
		 	SupLineList = []
		 	StatLineList = []
		 	TcpLineList = []
		 	index = 0		

		 	for lines in groupinfile:
		 
		 		#Split each line into different data types
		 		#Timestamp, TxSectorData, RxSectorData,  SNRData, RemoteSNRData , RSSIData ,UDPBandwidth, TCPBandwidth, BestBeamSNR, LastRemoteRssi,  LastBeaconRssi, LastDataRssi , CurrentMcs , RFTemp, BBTemp = lines.split(',')

		 		index = index+1 #Index start from zero
		 		
		 		Timestamp = lines.split(",")[0]
		 		TxSectorData = lines.split(",")[1]
		 		UDPBandwidth = lines.split(",")[6]
		 		BestBeamSNR = lines.split(",")[8]
		 		TCPBandwidth = lines.split(",")[7]

		 		Timestamplist = Timestamplist + [Timestamp] 

		 		if TxSectorData != "":
		 			SupLineList = SupLineList + [lines]
		 		
		 		if UDPBandwidth != "":
		 			UdpLineList = UdpLineList + [lines] # UDP lines when data is present


		 		if BestBeamSNR != "":
		 			StatLineList = StatLineList + [lines]

		 		if TCPBandwidth != "":
		 			TcpLineList = TcpLineList + [lines]
 
		#Start comparison of datatype (Stat or Sup) timestamp with Udp timestamps

		with open(str(inputlogfiledir)+"/Tsmergedata/Datatype/udp_type_" + filename, "wb") as datatypefile:
			writer = csv.DictWriter(datatypefile, fieldnames = ["Timestamp", "TxSectorData", "RxSectorData",  "SNRData", "RemoteSNRData" , "RSSIData" ,"UDP Bandwidth", "TCP Bandwidth", "BestBeamSNR (to Deci)", "LastRemoteRssi (to Deci)",  "LastBeaconRssi (to Deci)", "LastDataRssi (to Deci)" , "CurrentMcs (to Deci)" , "RFTemp (to Deci)", "BBTemp (to Deci)"], delimiter = ',' )
			writer.writeheader()

			for udpline in UdpLineList:

				timestampdifflist = []
				timestampdifflist2 = []

				udptimestampforline = float(udpline.split(' ')[0])
				timestampcheckbegin = udptimestampforline - udpchecktime

				for liness in StatLineList:
					timestampdifflist2 = timestampdifflist2 + [abs(float(liness.split(' ')[0]) - float(udpline.split(' ')[0]))] # Finding difference between timestamp of Udp and Stat data

				minvaluestatdata = min(timestampdifflist2)
				smallestvalueindex2 = timestampdifflist2.index(minvaluestatdata)
				Statdataofsmallestindexline = StatLineList[smallestvalueindex2]
				statdatatype = Statdataofsmallestindexline.split(",",8)[8]

				if "FAIL" not in statdatatype:

					BestBeamSNRData = statdatatype.split(',')[0]
					BestBeamSNRData = hex_to_dex(BestBeamSNRData)
					BestBeamSNRData = twos_comp(BestBeamSNRData, 8)
					

					LastRemoteRssiData = statdatatype.split(',')[1]
					LastRemoteRssiData = hex_to_dex(LastRemoteRssiData)
					LastRemoteRssiData = twos_comp(LastRemoteRssiData , 8)
					

					LastBeaconRssiData = statdatatype.split(',')[2]
					LastBeaconRssiData = hex_to_dex(LastBeaconRssiData) 
					LastBeaconRssiData = twos_comp(LastBeaconRssiData, 8)
	

					LastDataRssiData = statdatatype.split(',')[3]
					LastDataRssiData = hex_to_dex(LastDataRssiData)
					LastDataRssiData = twos_comp(LastDataRssiData, 8)
		

					CurrentMcsData = statdatatype.split(',')[4]
					CurrentMcsData = hex_to_dex(CurrentMcsData)

					RFTempData = statdatatype.split(',')[5]
					RFTempData = hex_to_dex(RFTempData)
					RFTempData = twos_comp(RFTempData, 16)
									

					BBTempData = statdatatype.split(',')[6]
					BBTempData =  hex_to_dex(BBTempData)
					BBTempData = twos_comp(BBTempData, 16)

				else:

					BestBeamSNRData = "FAIL"

					LastRemoteRssiData = "FAIL"

					LastBeaconRssiData = "FAIL"

					LastDataRssiData = "FAIL"

					CurrentMcsData = "FAIL"

					RFTempData = "FAIL"
				
					BBTempData = "FAIL"


				#udptimestamp = udpline.split(" ")[0]
				udpdatatype = udpline.split(",")[6]
				
				for lines in SupLineList:
					timestampsup = float(lines.split(' ')[0])
				
					if timestampsup >= timestampcheckbegin and timestampsup <= udptimestampforline:
						supcsvline = lines.rsplit(",",8)[0]
						
						supcsvline = str(supcsvline)  + udpdatatype + ",," +  str(BestBeamSNRData) + "," + str(LastRemoteRssiData) + "," + str(LastBeaconRssiData) + "," + str(LastDataRssiData) + "," + str(CurrentMcsData) + "," + str(RFTempData) + "," + str(BBTempData) + "\n"
						
						datatypefile.write(supcsvline)
						
				## To find the closest line to udp or tcp data ##
				#for lines in SupLineList:
					# timestampdifflist = timestampdifflist + [abs(float(lines.split(' ')[0]) - float(udpline.split(' ')[0]))] # Finding difference between timestamp of Udp and Sup data

				#minvaluesupdata = min(timestampdifflist)
				#smallestvalueindex = timestampdifflist.index(minvaluesupdata)

				#Supdataofsmallestindexline = SupLineList[smallestvalueindex]

				# supdatatype = Supdataofsmallestindexline.split(",",1)[1]	
				# supdatatype = supdatatype.rsplit(",",8)[0]
				

				BestBeamSNRData = ""

				LastRemoteRssiData = ""

				LastBeaconRssiData = ""

				LastDataRssiData = ""

				CurrentMcsData = ""

				RFTempData = ""
			
				BBTempData = ""


			# 	combineddata =  udpdatatype + ",,"  + str(BestBeamSNRData) + "," + str(LastRemoteRssiData) + "," + str(LastBeaconRssiData) + "," + str(LastDataRssiData) + "," + str(CurrentMcsData) + "," + str(RFTempData) + "," + str(BBTempData) + "\n"
				
			# 	datatypefile.write(combineddata)

			# combineddata = ""

		datatypefile.close()


		#Start comparison of datatype (Stat or Sup) timestamp with Udp timestamps

		with open(str(inputlogfiledir)+"/Tsmergedata/Datatype/tcp_type_" + filename, "wb") as tcpdatatypefile:
			writer = csv.DictWriter(tcpdatatypefile, fieldnames = ["Timestamp", "TxSectorData", "RxSectorData",  "SNRData", "RemoteSNRData" , "RSSIData" ,"UDP Bandwidth", "TCP Bandwidth", "BestBeamSNR (to Deci)", "LastRemoteRssi (to Deci)",  "LastBeaconRssi (to Deci)", "LastDataRssi (to Deci)" , "CurrentMcs (to Deci)" , "RFTemp (to Deci)", "BBTemp (to Deci)"], delimiter = ',' )
			writer.writeheader()

			# "vtcp" at the end of everything is a reference to tcp files
			for tcpline in TcpLineList:
				tcptimestampdifflist = []
				tcptimestampdifflist2 = []

				tcptimestampforline = float(tcpline.split(' ')[0])
				timestampcheckbeginvtcp = tcptimestampforline - tcpchecktime 


				for linesvtcp2 in StatLineList:
					tcptimestampdifflist2 = tcptimestampdifflist2 + [abs(float(linesvtcp2.split(' ')[0]) - float(tcpline.split(' ')[0]))] # Finding difference between timestamp of Udp and Stat data

				minvaluestatdatavtcp = min(tcptimestampdifflist2)
				smallestvalueindex2vtcp = tcptimestampdifflist2.index(minvaluestatdatavtcp)
				Statdataofsmallestindexlinevtcp = StatLineList[smallestvalueindex2vtcp]

				statdatatypevtcp = Statdataofsmallestindexlinevtcp.split(",",8)[8]

				if "FAIL" not in statdatatypevtcp:

					BestBeamSNRDatavtcp = statdatatypevtcp.split(',')[0]
					BestBeamSNRDatavtcp = hex_to_dex(BestBeamSNRDatavtcp)
					BestBeamSNRDatavtcp = twos_comp(BestBeamSNRDatavtcp, 8)
					

					LastRemoteRssiDatavtcp = statdatatypevtcp.split(',')[1]
					LastRemoteRssiDatavtcp = hex_to_dex(LastRemoteRssiDatavtcp)
					LastRemoteRssiDatavtcp = twos_comp(LastRemoteRssiDatavtcp , 8)
					

					LastBeaconRssiDatavtcp = statdatatypevtcp.split(',')[2]
					LastBeaconRssiDatavtcp = hex_to_dex(LastBeaconRssiDatavtcp) 
					LastBeaconRssiDatavtcp = twos_comp(LastBeaconRssiDatavtcp, 8)
	

					LastDataRssiDatavtcp = statdatatypevtcp.split(',')[3]
					LastDataRssiDatavtcp = hex_to_dex(LastDataRssiDatavtcp)
					LastDataRssiDatavtcp = twos_comp(LastDataRssiDatavtcp, 8)
		

					CurrentMcsDatavtcp = statdatatypevtcp.split(',')[4]
					CurrentMcsDatavtcp = hex_to_dex(CurrentMcsDatavtcp)

					RFTempDatavtcp = statdatatypevtcp.split(',')[5]
					RFTempDatavtcp = hex_to_dex(RFTempDatavtcp)
					RFTempDatavtcp = twos_comp(RFTempDatavtcp, 16)
									

					BBTempDatavtcp = statdatatypevtcp.split(',')[6]
					BBTempDatavtcp =  hex_to_dex(BBTempDatavtcp)
					BBTempDatavtcp = twos_comp(BBTempDatavtcp, 16)

				else:

					BestBeamSNRDatavtcp = "FAIL"

					LastRemoteRssiDatavtcp = "FAIL"

					LastBeaconRssiDatavtcp = "FAIL"

					LastDataRssiDatavtcp = "FAIL"

					CurrentMcsDatavtcp = "FAIL"

					RFTempDatavtcp = "FAIL"
				
					BBTempDatavtcp = "FAIL"

				#tcptimestamp = tcpline.split(" ")[0]
				tcpdatatype = tcpline.split(",")[7]

				for linesvtcp in SupLineList:
					timestampsupvtcp = float(linesvtcp.split(' ')[0])
					if timestampsupvtcp >= timestampcheckbeginvtcp and timestampsupvtcp <= tcptimestampforline:
						supcsvlinevtcp = linesvtcp.rsplit(",",8)[0]
						supcsvlinevtcp = str(supcsvlinevtcp) + "," + tcpdatatype + "," +  str(BestBeamSNRDatavtcp) + "," + str(LastRemoteRssiDatavtcp) + "," + str(LastBeaconRssiDatavtcp) + "," + str(LastDataRssiDatavtcp) + "," + str(CurrentMcsDatavtcp) + "," + str(RFTempDatavtcp) + "," + str(BBTempDatavtcp) + "\n"
						tcpdatatypefile.write(supcsvlinevtcp)


				## To find the closest line to udp or tcp data ##
				# for linesvtcp in SupLineList:
				# 	tcptimestampdifflist = tcptimestampdifflist + [abs(float(linesvtcp.split(' ')[0]) - float(tcpline.split(' ')[0]))] # Finding difference between timestamp of Udp and Sup data

				# minvaluesupdatavtcp = min(tcptimestampdifflist)
				# smallestvalueindexvtcp = tcptimestampdifflist.index(minvaluesupdatavtcp)

				# Supdataofsmallestindexlinevtcp = SupLineList[smallestvalueindexvtcp]


				# supdatatypevtcp = Supdataofsmallestindexlinevtcp.split(",",1)[1]	
				# supdatatypevtcp = supdatatypevtcp.rsplit(",",8)[0]
				
				

				BestBeamSNRDatavtcp = ""

				LastRemoteRssiDatavtcp = ""

				LastBeaconRssiDatavtcp = ""

				LastDataRssiDatavtcp = ""

				CurrentMcsDatavtcp = ""

				RFTempDatavtcp = ""
			
				BBTempDatavtcp = ""


				
			
			# 	combineddatavtcp = tcptimestamp + "," + supdatatypevtcp + "," + tcpdatatype + "," +  str(BestBeamSNRDatavtcp) + "," + str(LastRemoteRssiDatavtcp) + "," + str(LastBeaconRssiDatavtcp) + "," + str(LastDataRssiDatavtcp) + "," + str(CurrentMcsDatavtcp) + "," + str(RFTempDatavtcp) + "," + str(BBTempDatavtcp) + "\n"
				
			# 	tcpdatatypefile.write(combineddatavtcp)
				

			# combineddatavtcp = ""

		tcpdatatypefile.close()
		groupinfile.close()
		if filecount == 1:
			print ("File completed: " + str(filecount) + "/" + str(tsmergerfileCounter))
		else:
			print ("Files completed: " + str(filecount) + "/" + str(tsmergerfileCounter))
		filecount = filecount + 1


tsmergersummaryfileCounter = len(glob.glob1(inputlogfiledir + "/Tsmergedata/","output_tsmerge*_summary.csv"))
udpdatatypefileCounter = len(glob.glob1(inputlogfiledir + "/Tsmergedata/Datatype/","udp_type_*.csv"))
tcpdatatypefileCounter = len(glob.glob1(inputlogfiledir + "/Tsmergedata/Datatype/","tcp_type_*.csv"))

print "\nSummary:"
print "Input:"
print "Total number of output_tsmerged files in " + str(inputlogfiledir) + " is (" + str(tsmergerfileCounter) +")"
print "Output:"
print "Total number of output_tsmerged_summary files created is (" + str(tsmergersummaryfileCounter) + ") in " + str(inputlogfiledir + "/Tsmergedata")
print "Total number of udp_datatype files created is (" + str(udpdatatypefileCounter) + ") in " + str(inputlogfiledir + "/Tsmergedata/Datatype")
print "Total number of tcp_datatype files created is (" + str(tcpdatatypefileCounter) + ") in " + str(inputlogfiledir + "/Tsmergedata/Datatype")





