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

def ReceiveLVGreenSignal():
    while True:
        LowVoltageControlFileHandle = open(LowVoltageControlFileName, "r")
        GreenSignalState = str(LowVoltageControlFileHandle.read().strip())
        if GreenSignalState != "0": break
        time.sleep(0.5)
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

def WriteVoltageScanDataFile(ScanNumber, RunNumber, Voltage, MeasVoltage, MeasCurrent, Temp20):
    ScanDataFileHandle = open(VoltageScanDataFileName + 'scan' + str(ScanNumber) + '.txt' ,"a+")
    ScanDataFileHandle.write(str(RunNumber) + "\t" + str(Voltage) + "\t" + str(MeasVoltage) + "\t" + str(MeasCurrent) + "\t" + str(Temp20) + "\n")
    ScanDataFileHandle.close()

def ScopeStatusAutoPilot(runNumber):
    ScopeCommFile = open(ScopeCommFileName, "w")
    ScopeCommFile.write(str(runNumber))
    ScopeCommFile.close()
