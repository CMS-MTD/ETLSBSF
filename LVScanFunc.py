from AllModules import *
from FileComm import *

def InitiateResource():   # on keithley 2410 Menu->Communication->RS-232->Terminator-><LF>
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
            EnvTimestamp = (CurrentTime - datetime.strptime("2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")).total_seconds()# - 3600 #For daylight savings time
            if EnvTimestamp < 626058003.694: EnvTimestamp = EnvTimestamp
            #print "currenttime",CurrentTime
            Temp16,Temp20,Temp17,Temp18,Temp19 = ConvertEnv(EnvTimestamp)

            if ScanNumber>1:

                WriteEnvScanDataFile(ScanNumber, CurrentTime, MeasVoltage, MeasCurrent, Temp16,Temp20,Temp17,Temp18,Temp19)

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

def ReadVoltage(Resource):
    ReadCMD = ':READ?'
    ReadMeas = Resource.query(ReadCMD)
    VoltageReturned = float(ReadMeas.split(",")[0])
    CurrentReturned = float(ReadMeas.split(",")[1])

    return VoltageReturned, CurrentReturned


def IVScan(IVScanNumber, InitVoltage, FinalVoltage, voltage_step, VoltageSettleTime=10, MeasTimeInterval=5,  InitialSleepTime=5):

    Resource = InitiateResource()
    time.sleep(InitialSleepTime)
    ReadCMD = ':READ?'

    CurrentVoltage = 0
    while CurrentVoltage > InitVoltage:     
        SetVoltageCMD = ':SOUR:VOLT %f' % CurrentVoltage
        Resource.write(SetVoltageCMD)
        time.sleep(1)
        CurrentVoltage = CurrentVoltage - voltage_step
        if CurrentVoltage <= InitVoltage:
            CurrentVoltage = InitVoltage
            SetVoltageCMD = ':SOUR:VOLT %f' % CurrentVoltage
            Resource.write(SetVoltageCMD)

    voltage_up=[]
    voltage_down=[]
    current_up=[]
    current_down=[]

    # print CurrentVoltage, FinalVoltage
    while CurrentVoltage > FinalVoltage:

        SetVoltageCMD = ':SOUR:VOLT %f' % CurrentVoltage
        print 'Setting voltage to %i V' % CurrentVoltage
        Resource.write(SetVoltageCMD)

        i = 0
        while MeasTimeInterval * i < VoltageSettleTime:
            time.sleep(MeasTimeInterval)

            ReadMeas = Resource.query(ReadCMD)

            VoltageReturned = float(ReadMeas.split(",")[0])
            CurrentReturned = float(ReadMeas.split(",")[1])
            
            WriteIVScanDataFile(VoltageReturned, CurrentReturned, IVScanNumber)
            print VoltageReturned,CurrentReturned
            voltage_up.append(float(VoltageReturned))
            current_up.append(float(CurrentReturned))

            i = i + 1

        CurrentVoltage = CurrentVoltage + voltage_step
        if CurrentVoltage <= FinalVoltage:
            CurrentVoltage = FinalVoltage
            print 'Setting voltage to %i V' % CurrentVoltage
            SetVoltageCMD = ':SOUR:VOLT %f' % CurrentVoltage
            Resource.write(SetVoltageCMD)

    FinalVoltage = 0
    while CurrentVoltage < FinalVoltage:

        SetVoltageCMD = ':SOUR:VOLT %f' % CurrentVoltage
        Resource.write(SetVoltageCMD)

        i = 0
        while MeasTimeInterval * i < VoltageSettleTime:
            time.sleep(MeasTimeInterval)

            ReadMeas = Resource.query(ReadCMD)

            VoltageReturned = float(ReadMeas.split(",")[0])
            CurrentReturned = float(ReadMeas.split(",")[1])
            print VoltageReturned,CurrentReturned
            voltage_down.append(float(VoltageReturned))
            current_down.append(float(CurrentReturned))

            WriteIVScanDataFile(VoltageReturned, CurrentReturned, IVScanNumber)
            i = i + 1

        CurrentVoltage = CurrentVoltage - voltage_step
        if CurrentVoltage >= FinalVoltage:
            CurrentVoltage = FinalVoltage
            print 'Setting voltage to %i V' % CurrentVoltage
            SetVoltageCMD = ':SOUR:VOLT %f' % CurrentVoltage
            Resource.write(SetVoltageCMD)

    return voltage_up,current_up,voltage_down,current_down

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
    print "Trying to ramp up"
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