import requests
import ast
from datetime import datetime
import time
import numpy as np
import getpass
import os
import subprocess as sp
import socket
import sys
import glob
import subprocess
from subprocess import Popen, PIPE
import pipes
from pipes import quote
import argparse
import visa
import time
from GetEnv import *
from bisect import bisect_left
import getpass

#### OTSDAQ parameters ####
ip_address = "192.168.133.50"
use_socket = 8000
RunFilename = "/home/daq/otsdaq/srcs/otsdaq_cmstiming/Data_2018_09_September/ServiceData/RunNumber/OtherRuns0NextRunNumber.txt"
RunFilenameManual = "/home/daq/otsdaq/srcs/otsdaq_cmstiming/Data_2018_09_September/ServiceData/RunNumber/ManualRunNumber.txt"

laserMode=False
### Voltage Scan Parameters ###
InitialVoltage = -450
FinalVoltage = -560 #-650
numberOfOddVoltagesToSkip = 5 ### Skip every other bias point at the beginning of the scan, this many times.
nRunsPerVoltage = 2
nFinalVoltageRuns = 2 ##Number of runs at final voltage default should be one.
VoltageStep = -5
VoltageSettleTime = 300 #300#previously 10 #### BETWEEN EVERY RUN
MeasTimeInterval = 5 #Give an int, should be less than voltage settle time
InitialCurrentSettleTime = 3600#2*60*60#1500#1000 #5000 # time before first run [s]
Compliance = 50e-06 # 2e-06#18e-06
CurrRange = 1e-04#1e-05 #e-06 = microamps
ComplianceRange = 0.5e-06 #if the current reaches within this window around the compliance current, a warning will be sent to your email
VoltageRampDownSettleTime = 1
SBSFBaseDir = '/home/daq/BiasScan/ETLSBSF/'
ScanFilename = '%sNextScanNumber.txt' % SBSFBaseDir
LowVoltageControlFileName = '%sLVControl.txt' % SBSFBaseDir
VoltageScanDataFileName = '%sVoltageScanDataRegistry/' % SBSFBaseDir
IncludeLowVoltageFileName = '%sIncludeLowVoltageFile.txt' % SBSFBaseDir
StopAutopilotFileName = '%sStopAutopilot.sh' % SBSFBaseDir
ScopeCommFileName = '/home/daq/ETL_Agilent_MSO-X-92004A/Acquisition/ScopeStatus.txt'
NumEventsFileName = '%sNextNumEvents.txt' % SBSFBaseDir
ComplianceFileName = '%sComplianceFile.txt' % SBSFBaseDir

#Ensure compliance with foolish sign convention
if FinalVoltage > 0: FinalVoltage = -1 * FinalVoltage
if InitialVoltage > 0: InitialVoltage = -1 * InitialVoltage
if VoltageStep > 0: VoltageStep = -1 * VoltageStep
