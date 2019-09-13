echo "0" > /home/daq/BiasScan/LVControl.txt #Stop signal for LV Scan listener
echo "0" > /home/daq/BiasScan/IncludeLowVoltageFile.txt #Decouples autopilot and LVListener
echo "######## Stopping the LVScan gently! #######"