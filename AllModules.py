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

### Voltage Scan Parameters ###
InitialVoltage = -140 
#FinalVoltage = -600
FinalVoltage = -160 
VoltageStep = 10 
VoltageSettleTime = 10 #previously 10
Compliance = 1e-06
VoltageRampDownSettleTime = 1
SBSFBaseDir = '/home/daq/BiasScan/ETLSBSF/'
ScanFilename = '%sNextScanNumber.txt' % SBSFBaseDir
LowVoltageControlFileName = '%sLVControl.txt' % SBSFBaseDir
VoltageScanDataFileName = '%sVoltageScanDataRegistry/' % SBSFBaseDir
IncludeLowVoltageFileName = '%sIncludeLowVoltageFile.txt' % SBSFBaseDir
StopAutopilotFileName = '%sStopAutopilot.sh' % SBSFBaseDir
ScopeCommFileName = '/home/daq/ETL_Agilent_MSO-X-92004A/Acquisition/ScopeStatus.txt'
NumEventsFileName = '%sNextNumEvents.txt' % SBSFBaseDir

#Ensure compliance with foolish sign convention
if FinalVoltage > 0: FinalVoltage = -1 * FinalVoltage
if InitialVoltage > 0: InitialVoltage = -1 * InitialVoltage
if VoltageStep > 0: VoltageStep = -1 * VoltageStep


