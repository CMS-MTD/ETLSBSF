from AllModules import *

def GetNextNumber(RunOrScanFileName):
    FileHandle = open(RunOrScanFileName)
    nextNumber = int(FileHandle.read().strip())
    FileHandle.close()
    FileHandle = open(RunOrScanFileName,"w")
    FileHandle.write(str(nextNumber+1)+"\n") 
    FileHandle.close()
    return nextNumber

def GetNextNumEvents(NumEventsFileName):
    FileHandle = open(NumEventsFileName)
    NextNumEvents = int(FileHandle.read().strip())
    FileHandle.close()
    return NextNumEvents

def ReceiveLVGreenSignal(Resource, ScanNumber):
    i=0
    while True:

        MeasVoltage, MeasCurrent = Meas(Resource)
        CurrentTime = datetime.now()
        EnvTimestamp = (CurrentTime - datetime.strptime("2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")).total_seconds() - 3600 #For daylight savings time
        Temp16,Temp20,Temp17,Temp18,Temp19 = ConvertEnv(EnvTimestamp)

        if i % MeasTimeInterval == 0:
            WriteEnvScanDataFile(ScanNumber, CurrentTime, MeasVoltage, MeasCurrent, Temp16,Temp20,Temp17,Temp18,Temp19)
        i = i + 1

        LowVoltageControlFileHandle = open(LowVoltageControlFileName, "r")
        GreenSignalState = str(LowVoltageControlFileHandle.read().strip())
        if GreenSignalState != "0": break

        time.sleep(1) #should be 1 for meastimeinterval to make sense

    LowVoltageControlFileHandle.close()
    return int(GreenSignalState)

def ReceiveAutopilotGreenSignal():
    while True:        
        LowVoltageControlFileHandle = open(LowVoltageControlFileName, "r")
        GreenSignalState = str(LowVoltageControlFileHandle.read().strip())
        if GreenSignalState == "0": break
        time.sleep(0.5)
    LowVoltageControlFileHandle.close()
    return

def SendAutopilotGreenSignal():
    LowVoltageControlFileHandle = open(LowVoltageControlFileName, "w")
    LowVoltageControlFileHandle.write("0")
    LowVoltageControlFileHandle.close()

def SendLVGreenSignal(RunNumber):
    LowVoltageControlFileHandle = open(LowVoltageControlFileName, "w")
    LowVoltageControlFileHandle.write(str(RunNumber))
    LowVoltageControlFileHandle.close()
    return

def IncludeLowVoltageScan(IncludeBool):
    # Function to tell autopilot when to include Low voltage scan 
    IncludeLowVoltageHandle = open(IncludeLowVoltageFileName, "w")
    if IncludeBool:
        IncludeLowVoltageHandle.write("1")
    else:
        IncludeLowVoltageHandle.write("0")
    IncludeLowVoltageHandle.close()
    return

def LowVoltageBoolean():
    # Function that autopilot uses to find when to include LV Scan
    IncludeLowVoltageHandle = open(IncludeLowVoltageFileName, "r")
    LowVoltageBoolean = str(IncludeLowVoltageHandle.read().strip())
    if LowVoltageBoolean == "1":
        LVBool = True
    else:
        LVBool = False
    IncludeLowVoltageHandle.close()
    return LVBool

def WriteVoltageScanDataFile(ScanNumber, RunNumber, Voltage, MeasVoltage, MeasCurrent, Temp16,Temp20,Temp17,Temp18,Temp19,LaserTune):
    ScanDataFileHandle = open(VoltageScanDataFileName + 'scan' + str(ScanNumber) + '.txt' ,"a+")
    ScanDataFileHandle.write(str(RunNumber) + "\t" + str(Voltage) + "\t" + str(MeasVoltage) + "\t" + str(MeasCurrent) + "\t" + str(Temp16) + "\t" + str(Temp20) + "\t" + str(Temp17) + "\t" + str(Temp18) + "\t" + str(Temp19) + "\t" + str(LaserTune)+"\n" )
    ScanDataFileHandle.close()

def WriteEnvScanDataFile(ScanNumber, CurrentTime, MeasVoltage, MeasCurrent, Temp16,Temp20,Temp17,Temp18,Temp19):
    ScanDataFileHandle = open(VoltageScanDataFileName + 'EnvScan' + str(ScanNumber) + '.txt' ,"a+")
    ScanDataFileHandle.write(str(CurrentTime) + "\t" + str(MeasVoltage) + "\t" + str(MeasCurrent) + "\t" + str(Temp16) + "\t" + str(Temp20) + "\t" + str(Temp17) + "\t" + str(Temp18) + "\t" + str(Temp19) + "\n")
    ScanDataFileHandle.close()

#def ReadVoltageScanDataFile(ScanNumber):
#    ScanDataFileHandle = open(VoltageScanDataFileName + 'scan' + str(ScanNumber) + '.txt' ,"a+")
#    FirstEntry = ScanDataFileHandle.read().split('\n')[0].split('\t')
#    MaxVoltage = FirstEntry[0] 
#    ScanDataFileHandle.close()

def ScopeStatusAutoPilot(runNumber):
    ScopeCommFile = open(ScopeCommFileName, "w")
    ScopeCommFile.write(str(runNumber))
    ScopeCommFile.close()

def WriteTimeScanDataFile(Voltage, Current, TimeDiff, FileNumber):
    ScanDataFileHandle = open(VoltageScanDataFileName + 'Timescan' + str(FileNumber) + '.txt' ,"a+")
    ScanDataFileHandle.write(str(Voltage) + "\t" + str(Current) + "\t" + str(TimeDiff) + "\n")
    ScanDataFileHandle.close()

def WriteIVScanDataFile(Voltage, Current, FileNumber):
    ScanDataFileHandle = open(VoltageScanDataFileName + 'IVScan' + str(FileNumber) + '.txt' ,"a+")
    ScanDataFileHandle.write(str(Voltage) + "\t" + str(Current) + "\n")
    ScanDataFileHandle.close()

def HitComplianceTrue():
    ComplianceFileHandle = open(ComplianceFileName, "w")
    ComplianceFileHandle.write("1")
    ComplianceFileHandle.close()

def ReadCompliance():
    # Function that autopilot uses to find when to include LV Scan
    IncludeLowVoltageHandle = open(ComplianceFileName, "r")
    LowVoltageBoolean = str(IncludeLowVoltageHandle.read().strip())
    if LowVoltageBoolean == "1":
        LVBool = True
    else:
        LVBool = False
    IncludeLowVoltageHandle.close()
    return LVBool

def Meas(Resource):
    ReadCMD = ':READ?'
    ReadMeas = "-1.0,-1.0"
    try:
        ReadMeas = Resource.query(ReadCMD)
    except:
        time.sleep(5)
        try:
            ReadMeas = Resource.query(ReadCMD)
        except pyvisa.errors.VisaIOError as e:
            print "Error: {}".format(e)

    VoltageReturned = float(ReadMeas.split(",")[0])
    CurrentReturned = float(ReadMeas.split(",")[1])

    return VoltageReturned, CurrentReturned