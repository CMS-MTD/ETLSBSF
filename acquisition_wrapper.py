from AllModules import *
from FileComm import *
### if sample rate or horizontal window is changed, TimingDAQ must be recompiled to account for new npoints.
sampleRate = 20#40 #20 #GSa/s
horizontalWindow = 50 #ns

#Hard Code these:
trigCh = "4" 
trig = -0.01#-0.01 #-0.01 #V

vScale1 = 0.05
vScale2 = 0.05 
vScale3 = 0.05 #0.07 #0.05 
vScale4 = 0.01 #0.01 

trigSlope = "NEG"
timeoffset = 0 #ns

if laserMode: 
	trigCh="1"
	trig =0.6
	trigSlope="POS"
	vScale1 = 1.
	vScale2 = 0.10
	vScale3 = 0.2
	timeoffset=55

LecroyMode = True
if LecroyMode:
	timeoffset=0.
	sampleRate=10 #probably doesn't work in script, make sure is correct manually
	trigCh="C4"
	trig=-0.01

RunNumber = -1


ScopeControlDir =  "/home/daq/ETL_Agilent_MSO-X-92004A/"
# AutoPilotStatusFile = '%sAcquisition/ScopeStatus.txt' % ScopeControlDir
if LecroyMode:

	ScopeControlDir = "/home/daq/ScopeHandler/Lecroy/"

def ScopeAcquisition(RunNumber, NumEvents):
	if RunNumber == -1: 
		RunNumber = GetNextNumber(RunFilenameManual)
	print "\n ####################### Running the scope acquisition ##################################\n"
	AgilentScopeCommand = 'python %sAcquisition/acquisition.py --runNum %s --numEvents %d --sampleRate %d --horizontalWindow %d --trigCh %s --trig %f --vScale1 %f --vScale2 %f --vScale3 %f --vScale4 %f --timeoffset %i --trigSlope %s --display 1' % (ScopeControlDir,RunNumber, NumEvents, sampleRate, horizontalWindow, trigCh, trig, vScale1, vScale2, vScale3, vScale4, timeoffset, trigSlope) 
	
	print AgilentScopeCommand
	os.system(AgilentScopeCommand)
		    

if __name__ == "__main__":
	NumEvents = int(sys.argv[1])
	ScopeAcquisition(RunNumber,NumEvents)
