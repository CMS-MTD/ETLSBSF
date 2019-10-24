from AllModules import *
from FileComm import *

def InitiateResource():
    #CMD =':CONF:VOLT' #COnfiguring voltage as the output
    SourFuncCMD =':SOUR:FUNC VOLT'
    SensFuncCMD = 'SENS:FUNC "CURR"'

    VoltRangeCMD =':SOUR:VOLT:RANG %f' % FinalVoltage
    CurrRangeCMD =':SENS:CURR:RANG %f' % CurrRange
    
    SensSpeedCMD = 'SENS:CURR:NPLC 10'   
    ComplianceCMD = ':SENS:CURR:PROT %f' % Compliance
    
    OutputONCMD = ':OUTP ON'

    VISAInstance=visa.ResourceManager('@py')
    ResourceList=VISAInstance.list_resources()
    for index in range(len(ResourceList)):
        print("Device number " + str(index) + " - " + ResourceList[index])
    DeviceNumber = raw_input("Which device would you like to use?")
    Resource = VISAInstance.open_resource(ResourceList[int(DeviceNumber)])
    
    Resource.write(SourFuncCMD)
    Resource.write(SensFuncCMD)

    Resource.write(VoltRangeCMD)
    Resource.write(CurrRangeCMD)
    
    Resource.write(SensSpeedCMD)
    Resource.write(ComplianceCMD)

    Resource.write(OutputONCMD)
    return Resource

def SetVoltage(Resource, ScanNumber, Voltage, VoltageSettleTime = 15, Debug = False):
    if Debug: print(Resource.query("*idn?"))

    #VoltageMeasCMD =':MEAS:VOLT?'
    #CurrentMeasCMD =':MEAS:CURR?'

    SetVoltageCMD = ':SOUR:VOLT %f' % Voltage
    ReadCMD = ':READ?'

    Resource.write(SetVoltageCMD)
    
    if not Debug:
        print 'Sleeping for %ds, for current to settle' % VoltageSettleTime
        i = 0
        while MeasTimeInterval * i <= VoltageSettleTime:
            ReadMeas = Resource.query(ReadCMD)

            MeasVoltage = float(ReadMeas.split(",")[0])
            MeasCurrent = float(ReadMeas.split(",")[1])

            CurrentTime = datetime.now()
            EnvTimestamp = (CurrentTime - datetime.strptime("2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")).total_seconds() - 3600 #For daylight savings time
            Temp20 = ConvertEnv(EnvTimestamp)

            WriteEnvScanDataFile(ScanNumber, CurrentTime, MeasVoltage, MeasCurrent, Temp20)

            time.sleep(MeasTimeInterval)
            
            i = i + 1
        #time.sleep(VoltageSettleTime)
        print 'Now returning the program flow to Autopilot'

    #VoltageMeasurement = Resource.query(VoltageMeasCMD)
    #VoltageMeasurement = Resource.query(VoltageMeasCMD) # Have to do it twice
    #CurrRangeCMD =':SENS:CURR:RANG AUTO'

    #CurrentMeasurement = Resource.query(CurrentMeasCMD)
    #CurrentMeasurement = Resource.query(CurrentMeasCMD)

    ReadMeas = Resource.query(ReadCMD)

    VoltageReturned = float(ReadMeas.split(",")[0])
    CurrentReturned = float(ReadMeas.split(",")[1])

    #print CurrentReturned
    return VoltageReturned, CurrentReturned


def IVScan(FinalVoltage, VoltageSettleTime, IVScanNumber, InitialSleepTime):

    Resource = InitiateResource()
    time.sleep(InitialSleepTime)
    ReadCMD = ':READ?'

    CurrentVoltage = -10
    MeasTimeInterval = 10
    VoltageList = []
    CurrentList = []

    while CurrentVoltage > FinalVoltage:

        SetVoltageCMD = ':SOUR:VOLT %f' % CurrentVoltage
        Resource.write(SetVoltageCMD)

        i = 0
        while MeasTimeInterval * i <= VoltageSettleTime:
            time.sleep(MeasTimeInterval)

            ReadMeas = Resource.query(ReadCMD)

            VoltageReturned = float(ReadMeas.split(",")[0])
            CurrentReturned = float(ReadMeas.split(",")[1])
            
            VoltageList.append(VoltageReturned)            
            CurrentList.append(CurrentReturned)
            WriteIVScanDataFile(VoltageReturned, CurrentReturned, IVScanNumber)
            i = i + 1

        CurrentVoltage = CurrentVoltage - 10
        if CurrentVoltage <= FinalVoltage:
            CurrentVoltage = FinalVoltage
            SetVoltageCMD = ':SOUR:VOLT %f' % CurrentVoltage
            Resource.write(SetVoltageCMD)

    FinalVoltage = 0
    while CurrentVoltage < FinalVoltage:

        SetVoltageCMD = ':SOUR:VOLT %f' % CurrentVoltage
        Resource.write(SetVoltageCMD)

        i = 0
        while MeasTimeInterval * i <= VoltageSettleTime:
            time.sleep(MeasTimeInterval)

            ReadMeas = Resource.query(ReadCMD)

            VoltageReturned = float(ReadMeas.split(",")[0])
            CurrentReturned = float(ReadMeas.split(",")[1])
            
            VoltageList.append(VoltageReturned)            
            CurrentList.append(CurrentReturned)
            WriteIVScanDataFile(VoltageReturned, CurrentReturned, IVScanNumber)
            i = i + 1

        CurrentVoltage = CurrentVoltage + 10
        if CurrentVoltage >= FinalVoltage:
            CurrentVoltage = FinalVoltage
            SetVoltageCMD = ':SOUR:VOLT %f' % CurrentVoltage
            Resource.write(SetVoltageCMD)

def TimeScan(Voltage, Time, FileNumber):
    #import matplotlib.pyplot as plt

    Resource = InitiateResource()
    RampUp(Resource, Voltage)

    SetVoltageCMD = ':SOUR:VOLT %f' % Voltage
    ReadCMD = ':READ?'

    VoltageList = []
    CurrentList = []


    StartTime = datetime.now()

    while True:
        time.sleep(Time)

        ReadMeas = Resource.query(ReadCMD)

        VoltageReturned = float(ReadMeas.split(",")[0])
        CurrentReturned = float(ReadMeas.split(",")[1])
        
        VoltageList.append(VoltageReturned)            
        CurrentList.append(CurrentReturned)

        TimeNow = datetime.now()
        TimeDiff = (TimeNow - StartTime).total_seconds()
        WriteTimeScanDataFile(VoltageReturned, CurrentReturned, TimeDiff, FileNumber)

def RampUp(Resource, StartVoltage, Debug = False):
    if Debug: print(Resource.query("*idn?"))

    CurrentVoltage = 0
    while CurrentVoltage > StartVoltage:     
        SetVoltageCMD = ':SOUR:VOLT %f' % CurrentVoltage
        Resource.write(SetVoltageCMD)
        time.sleep(1)
        CurrentVoltage = CurrentVoltage - 10
        if CurrentVoltage <= StartVoltage:
            CurrentVoltage = StartVoltage
            SetVoltageCMD = ':SOUR:VOLT %f' % CurrentVoltage
            Resource.write(SetVoltageCMD)

def RampDown(Resource, Voltage, VoltageSettleTime = 5, Debug = False):
    if Debug: print(Resource.query("*idn?"))
    ReadCMD = ':READ?'

    CurrentVoltage = Voltage
    while CurrentVoltage < 0:     
        SetVoltageCMD = ':SOUR:VOLT %f' % CurrentVoltage
        Resource.write(SetVoltageCMD)
        time.sleep(VoltageSettleTime)
        
        ReadMeas = Resource.query(ReadCMD)

        VoltageReturned = float(ReadMeas.split(",")[0])
        print 'Now the voltage is ', VoltageReturned

        CurrentVoltage = CurrentVoltage + 10
        if CurrentVoltage >= 0:
            CurrentVoltage = 0
            SetVoltageCMD = ':SOUR:VOLT %f' % CurrentVoltage
            Resource.write(SetVoltageCMD)

    DisableLVOutput(Resource)

def DisableLVOutput(Resource):
    OutputOFFCMD = ':OUTP:STAT OFF'
    Resource.write(OutputOFFCMD)