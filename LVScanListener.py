from LVScanFunc import * 
from FileComm import *
from AllModules import *

BoardName = raw_input("Board Name : ") 
SensorName = raw_input("Sensor Name : ")
ChillerTemp = raw_input("ChillerTemperature (C): ")
LaserTune = raw_input("LaserTune [%] (enter 0 for beta source): ")

Resource = InitiateResource()
StartTime = datetime.now() 
Voltage = InitialVoltage

IncludeLowVoltageScan(True) #Tells Autopilot to include low voltage scan

if LowVoltageBoolean():
    ScanNumber = GetNextNumber(ScanFilename)
    print "\n*********************** Starting scan %d ****************************" % ScanNumber

RampUp(Resource, InitialVoltage, False)

time.sleep(InitialCurrentSettleTime)

StartRunNumber = -1
changeVoltage = True
runsAtCurrentVoltage=0
while abs(Voltage) <= abs(FinalVoltage) and nFinalVoltageRuns>0:
    print '\n*************************'
    print 'Waiting for the green signal from the autopilot\n'
    RunNumber = ReceiveLVGreenSignal(Resource, ScanNumber)
    if StartRunNumber ==-1:
        StartRunNumber = RunNumber
    if RunNumber != 0:
        EnvTimestamp = (datetime.now() - datetime.strptime("2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")).total_seconds() #For daylight savings time
        Temp16,Temp20,Temp17,Temp18,Temp19 = ConvertEnv(EnvTimestamp)


        #if abs(Voltage) <= abs(FinalVoltage):
        if changeVoltage:
            print 'Changing the Voltage to %f V' % Voltage
            MeasVoltage, MeasCurrent = SetVoltage(Resource, ScanNumber, Voltage, VoltageSettleTime, False)
            if nRunsPerVoltage>1:
                WriteVoltageScanDataFile(ScanNumber, "%i-%i"%(int(RunNumber),int(RunNumber)+nRunsPerVoltage-1), Voltage, MeasVoltage, MeasCurrent, Temp16,Temp20,Temp17,Temp18,Temp19,LaserTune)
            else:
                WriteVoltageScanDataFile(ScanNumber, RunNumber, Voltage, MeasVoltage, MeasCurrent, Temp16,Temp20,Temp17,Temp18,Temp19,LaserTune)

        else:
            print "Taking an extra run at {} V".format(round(Voltage,2))
            print 'Reading the current for extra run'
            time.sleep(5)
            MeasVoltage,MeasCurrent = ReadVoltage(Resource)
    
        if Compliance - MeasCurrent < ComplianceRange :
            HitComplianceTrue()



        ##### Write scan data for this run
        if Voltage == FinalVoltage:
            nFinalVoltageRuns = nFinalVoltageRuns-1
            nRunsPerVoltage=1
            if not changeVoltage: WriteVoltageScanDataFile(ScanNumber, RunNumber, Voltage, MeasVoltage, MeasCurrent, Temp16,Temp20,Temp17,Temp18,Temp19,LaserTune)
            changeVoltage = False

        runsAtCurrentVoltage = runsAtCurrentVoltage+1
        if runsAtCurrentVoltage < nRunsPerVoltage:
            changeVoltage=False
        else:
            changeVoltage=True
            runsAtCurrentVoltage=0

            if Voltage != FinalVoltage:
                Voltage = Voltage + VoltageStep
                if numberOfOddVoltagesToSkip > 0: 
                    Voltage = Voltage + VoltageStep
                    numberOfOddVoltagesToSkip = numberOfOddVoltagesToSkip - 1


        #if InitialVoltage != FinalVoltage:


        #if abs(Voltage) > abs(FinalVoltage):
            
            #StopAutopilot = raw_input("This is the last allowed voltage value. Do you want to stop the autopilot after this iteration (y/n) ? ")
            # if StopAutopilot == "y" or StopAutopilot == "Y" : 
            #     os.system("source %s" % StopAutopilotFileName)
            # else:
            #     print 'Now the autopilot will keep on taking data even after the scan completes, at Voltage %f V' % (Voltage - VoltageStep)
            #     IncludeLowVoltageScan(False) # Tells Autopilot to keep on running without including the LV scan program
           
        print 'The current run number is ', RunNumber
        print '*************************\n'

        SendAutopilotGreenSignal()


ReceiveLVGreenSignal(Resource, ScanNumber)
##Ryan: always ramp down
#DisableOutput = raw_input("Ramp down (y), disable Low Voltage Output (n)?")
# if  DisableOutput == "y" or DisableOutput == "Y" :
#     RampDown(Resource, Voltage - VoltageStep, VoltageRampDownSettleTime, False)
# if  DisableOutput == "n" or DisableOutput == "N" :
#     DisableLVOutput(Resource)
os.system("source %s" % StopAutopilotFileName)
RampDown(Resource, Voltage - VoltageStep, VoltageRampDownSettleTime, False)
SendAutopilotGreenSignal() ## ask autopilot to stop

StopTime = datetime.now()
print "\n*********************** Scan %d complete ****************************" % ScanNumber
print '%d,%s,%s,%d,%d,%s,%s,%s,%f,%i,%i,%s' %(ScanNumber, str(StartTime), str(StopTime), StartRunNumber, RunNumber, SensorName,BoardName, ChillerTemp, Temp16, FinalVoltage, VoltageStep,LaserTune)