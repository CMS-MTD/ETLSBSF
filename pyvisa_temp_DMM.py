import visa
import time
import sys

def getResourceDMM(debug=False):    
    # Setup resource that will talk to DMM
    rm = visa.ResourceManager('@py')

    # Connect to DMM and setup default settings
    #my_instrument = rm.open_resource('ASRL/dev/ttyUSB0::INSTR') #KEITHLEY INSTRUMENTS INC.,MODEL 2410,4105344,C33   Mar 31 2015 09:32:39/A02  /J/K
    #my_instrument = rm.open_resource('TCPIP0::192.168.133.159::inst0::INSTR') #KEYSIGHT TECHNOLOGIES,MSOX92004A,MY53240102,05.70.00901
    #my_instrument = rm.open_resource('TCPIP0::192.168.133.169::inst0::INSTR') #LECROY,WR8208HD,LCRY5003N60377,9.4.0
    my_instrument = rm.open_resource('TCPIP::192.168.133.53::1394::SOCKET') #Keithley DMM
    my_instrument.write("*RST; status:preset; *CLS")
    my_instrument.write("TEMP:TRAN FRTD")
    my_instrument.read_termination = '\n'
    my_instrument.write_termination = '\n'
    my_instrument.timeout = 5000
    my_instrument.baud_rate = 57600

    # Print stuff for debugging if needed
    if debug:
        print(rm.list_resources())
        print(my_instrument.query('*IDN?'))

    return my_instrument

def queryVal(my_instrument, cmd):
    # Query intrument 
    val = str(my_instrument.query(cmd))

    # Parse output of pyvisa and convert to float
    val = val.split(",")[0]
    try:
        val = float(val[1:])
    except:
        try:
            val = float(val[1:-2])
        except:
            raise ValueError('Could not convert string to float: ', val)

    return val

def queryMultiVal(my_instrument, cmd, channels):
    t = round(time.time(), 3)
    vals = []
    for ch, doRead in channels:
        val = 0
        if doRead:
            val = queryVal(my_instrument, "{0} (@{1})".format(cmd, ch))
        vals.append(val)

    line = "{:.15f}\t".format(t)
    for x in vals:
        line += "{:.15f}\t".format(x)
        
    return line

def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()        
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()

def main():
    print("Start logging temp")
    my_instrument = getResourceDMM()
    print("Connected to multi-meter")
    
    minChannel = 94; maxChannel = 132
    readChannels = [112]
    entriesPerLogFile = 100
    allChannels = list((channel,True if channel in readChannels else False) for channel in range(minChannel,maxChannel+1))
    
    try:
        while True:
            fileName = "tempLogs/lab_meas_unsync_{:.3f}.txt".format(time.time())
            print("-"*50)
            print("Sending measured temperature to: {}".format(fileName))
            f = open(fileName,"w")
    
            lineCounter = 0
            for lineCounter in progressbar(range(entriesPerLogFile), "  Filling log file: ", 40):
                line = queryMultiVal(my_instrument, 'MEAS:TEMP?', allChannels)
                f.write(line+"\n")
                time.sleep(1)
            f.close()
    except KeyboardInterrupt:
        print("\nStopped the logging of temperature")
        if f:
            f.close()
        pass
    
if __name__ == "__main__":
    main()

