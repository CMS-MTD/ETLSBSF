from AllModules import *

def init_ots():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MESSAGE = "OtherRuns0,Initialize"
    sock.sendto(MESSAGE, (ip_address, use_socket))
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "Initialize: received message:", data
    time.sleep(5)

def config_ots():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MESSAGE = "OtherRuns0,Configure,FQNETConfig"
    sock.sendto(MESSAGE, (ip_address, use_socket))
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "Configure: received message:", data
    time.sleep(5)

def start_ots(RunNumber, Delay):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MESSAGE = "OtherRuns0,Start, %d" % (RunNumber)#(GetRunNumber()+1)
    sock.sendto(MESSAGE, (ip_address, use_socket))
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes                                                                                                                                                                              
    print "Start: received message : ", data
    return 
    
def stop_ots(Delay):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MESSAGE = "OtherRuns0,Stop"
    sock.sendto(MESSAGE, (ip_address, use_socket))
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes                                                                                                                                                                              
    print "Stop: received message : ", data
    if Delay: time.sleep(5)