import argparse
import commands
import time
import os
from FileComm import *

parser = argparse.ArgumentParser()
parser.add_argument ('-d', '--disk', type=str, default='/home', help='Disk or volume to check')
parser.add_argument ('-l', '--limit', type=str, default='20G', help='Limit disk space')
parser.add_argument('-e', '--email', help='delimited list input', default="'merajwarn@gmail.com', 'rheller@fnal.gov','apresyan@fnal.gov', 'kdipetrillo@gmail.com' ", type=str)
args = parser.parse_args()

EmailList = [str(item) for item in args.email.split(',')]

args = parser.parse_args()

size_dic = {'P': 1024**5, 'T': 1024**4, 'G':1024**3, 'M':1024**2, 'K': 1024}

Nlim =  float(args.limit[:-1])*size_dic[args.limit[-1]]

MemoryAlert = False
DontCheckMemory = False
DontCheckCompliance = False
ComplianceHitBool = False

while(True):

	if not MemoryAlert and not DontCheckMemory:	
		_, out = commands.getstatusoutput('df -h | grep \"' + args.disk + '\"')
		out = [x for x in out.split(' ') if x]

		sfree = out[3]
		Nfree = float(sfree[:-1])*size_dic[sfree[-1]]

		MemoryAlert = Nfree <= Nlim
	else:
		print "Memory limit email already sent. Now will monitor compliance only"
		MemoryAlert = False


	if not ComplianceHitBool and not DontCheckCompliance:
		ComplianceHitBool = ReadCompliance()
	else:
		print "compliance limit email already sent. Now will monitor memory only"
		ComplianceHitBool = False

	if DontCheckCompliance and DontCheckMemory:
		break

	if MemoryAlert or ComplianceHitBool:
		print time.ctime(time.time())

		if ComplianceHitBool:
			DontCheckCompliance = True
			#print 'Current compliance Limit reached!'
			subject = 'Current reached compliance on the Keithley!'
			warning = '[WARNING]: Current has reached compliance\n\n'
		else:
			DontCheckMemory = True
			subject = 'Limit memory reached on TimingDAQ01!'
			warning = '[WARNING]: Only {} free left on disk {} ({})\n\n'.format(sfree, out[0], out[-1])
					
		print 'Sending an email\n'
		if args.email:
			cmd = 'echo \"'+ warning + '\" | mail -s \"'+subject+'\" ' + ','.join(EmailList)
			os.system(cmd)

		if MemoryAlert and ComplianceHitBool:
			break
	
	time.sleep(300)

