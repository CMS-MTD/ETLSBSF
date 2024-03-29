from TCPComm import *  
from FileComm import *
from AllModules import *
from acquisition_wrapper import *

#################################Parsing arguments######################################
parser = argparse.ArgumentParser(description='Information for running the AutoPilot program. /n /n General Instructions: Start OTSDAQ and Configure by hand.')
parser.add_argument('-rd', '--RunDuration', type=float,required=True)
Debug = True

args = parser.parse_args()
RunDuration = args.RunDuration

# Use Status file to tell autopilot when to stop.
if os.path.exists("AutoPilot.status"):
	os.remove("AutoPilot.status")
statusFile = open("AutoPilot.status","w") 
statusFile.write("START") 
statusFile.close() 
AutoPilotStatus = 1


print "*********************************************************************"
print "######################## Starting AutoPilot #########################"
print "*********************************************************************"
firstRun=-1
lastRun=-1
StartTime = datetime.now() 
while AutoPilotStatus == 1:
	

	### Function to read run number and increment it in the file
	RunNumber = GetNextNumber(RunFilename)
	if firstRun==-1: firstRun=RunNumber
	NumEvents = GetNextNumEvents(NumEventsFileName)
	print 'Going to use NumEvents %d for the next scope run' % NumEvents

	####### Incrementing the Intereferometer low voltage ########
	if LowVoltageBoolean(): 
		print 'Sending Low Voltage Supply a signal to increment the voltage'
		SendLVGreenSignal(RunNumber) 
		print 'Waiting for the Low Voltage Supply to complete the action'
		ReceiveAutopilotGreenSignal()
		print 'Supply has ramped up.'
		#################################################
		#Check for Stop signal in AutoPilot.status file
		#################################################
		tmpStatusFile = open("AutoPilot.status","r") 
		tmpString = (tmpStatusFile.read().split())[0]
		if (tmpString == "STOP" or tmpString == "stop"):
			print "Detected stop signal.\nStopping AutoPilot ...\n\n"
			AutoPilotStatus = 0
			continue

		#Send aquisition command to the scope
		print 'Starting scope.'
		ScopeAcquisition(RunNumber, NumEvents)
		lastRun=RunNumber

 
	print "\nRun %i starting" % (RunNumber)

	if not Debug: start_ots(RunNumber,False)

	#time.sleep(RunDuration)

	if not Debug: stop_ots(False)

	print "\nRun %i stopped" % (RunNumber)
	print "\n*********************************************************************"



StopTime = datetime.now()
tmpStatusFile.close()


print "\n*********************************************************************"
print "######################## AutoPilot Stopped ##########################"
print "*********************************************************************"
