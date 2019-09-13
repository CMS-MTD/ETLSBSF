from AllModules import *

def InitiateResource():
    CMD =':CONF:VOLT' #COnfiguring voltage as the output
    VoltRangeCMD =':SOUR:VOLT:RANG %f' % FinalVoltage
    ComplianceCMD = ':SENS:CURR:PROT %f' % Compliance
    VISAInstance=visa.ResourceManager('@py')
    ResourceList=VISAInstance.list_resources()
    for index in range(len(ResourceList)):
        print("Device number " + str(index) + " - " + ResourceList[index])
    DeviceNumber = raw_input("Which device would you like to use?")
    Resource = VISAInstance.open_resource(ResourceList[int(DeviceNumber)])
    Resource.write(CMD)
    Resource.write(VoltRangeCMD)
    Resource.write(ComplianceCMD)
    return Resource

def SetVoltage(Resource, Voltage, VoltageSettleTime = 15, Debug = False):
    if Debug: print(Resource.query("*idn?"))

    VoltageMeasCMD =':MEAS:VOLT?'
    CurrentMeasCMD =':MEAS:CURR?'

    SetVoltageCMD = ':SOUR:VOLT %f' % Voltage

    Resource.write(SetVoltageCMD)

    if not Debug:
        print 'Sleeping for %ds, for current to settle' % VoltageSettleTime
        time.sleep(VoltageSettleTime)
        print 'Now returning the program flow to Autopilot'

    VoltageMeasurement = Resource.query(VoltageMeasCMD)
    VoltageMeasurement = Resource.query(VoltageMeasCMD) # Have to do it twice

    CurrentMeasurement = Resource.query(CurrentMeasCMD)
    CurrentMeasurement = Resource.query(CurrentMeasCMD)


    VoltageReturned = float(VoltageMeasurement.split(",")[0])
    CurrentReturned = float(CurrentMeasurement.split(",")[1])

    return VoltageReturned, CurrentReturned

def RampUp(Resource, StartVoltage, Debug = False):
    if Debug: print(Resource.query("*idn?"))

    VoltageMeasCMD =':MEAS:VOLT?'
    CurrentMeasCMD =':MEAS:CURR?'

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

    VoltageMeasCMD =':MEAS:VOLT?'
    CurrentMeasCMD =':MEAS:CURR?'

    CurrentVoltage = Voltage
    while CurrentVoltage < 0:     
        SetVoltageCMD = ':SOUR:VOLT %f' % CurrentVoltage
        Resource.write(SetVoltageCMD)
        time.sleep(VoltageSettleTime)
        CurrentVoltage = CurrentVoltage + 10
        if CurrentVoltage >= 0:
            CurrentVoltage = 0
            SetVoltageCMD = ':SOUR:VOLT %f' % CurrentVoltage
            Resource.write(SetVoltageCMD)

    DisableLVOutput(Resource)

def DisableLVOutput(Resource):
    OutputOFFCMD = ':OUTP:STAT OFF'
    Resource.write(OutputOFFCMD)