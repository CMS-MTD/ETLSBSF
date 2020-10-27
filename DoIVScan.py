from LVScanFunc import * 
from FileComm import *
from AllModules import *

# import ROOT

SensorName = raw_input("Sensor Name : ")
ChillerTemp = raw_input("ChillerTemperature (C): ")
initial_voltage = int(raw_input("Start voltage [V]: "))
final_voltage = int(raw_input("End voltage [V]: "))
voltage_step = int(raw_input("Step [V]: "))

ScanNumber = GetNextNumber("NextIVNumber.txt")

# Resource = InitiateResource()
# StartTime = datetime.now() 

if final_voltage > 0: final_voltage = -1 * final_voltage
if initial_voltage > 0: initial_voltage = -1 * initial_voltage
if voltage_step > 0: voltage_step = -1 * voltage_step

# print initial_voltage,final_voltage,voltage_step
# v_up,i_up,v_down,i_down = 
IVScan(ScanNumber, initial_voltage, final_voltage, voltage_step)


# c1 =ROOT.TCanvas()

# graph_up = ROOT.TGraphErrors(len(v_up),array("d",v_up),array("d",i_up),array("d",[0.1 for i in v_up]),array("d",[1e-12 for i in i_up]))
# graph_down = ROOT.TGraphErrors(len(v_down),array("d",v_down),array("d",i_down),array("d",[0.1 for i in v_down]),array("d",[1e-12 for i in i_down]))

# graph_up.Draw("AELP")
# c1.Print("testIV.pdf")