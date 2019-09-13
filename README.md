# SBSF
Source Bias Scan Framework

Instructions for running scan:

1) Make sure HV is supplied to LGAD from TOP keithley
2) Start Sidet_Labview.gvi with only the DMM enabled (no sourcemeter). No need to restart between scans
3) Make sure motors are in appropriate position
4) Make sure photodiode and all testing channels are returned to VME
5) Specify scan parameters in AllModules.py
6) start listener: python LVScanListener.py (dedicated tab). Use option 2 when prompted
7) ./RunAutopilot.sh


Plotting results:
1) Make new series text file or add entry to existing one in LBSF/Plotter/series/. Filename must be SeriesN.txt
2) python plot_bias_scan.py seriesNum
3) Plots appear in plots directory.
