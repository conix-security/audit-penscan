'''
plugin Smb
triggers=
ports=445
'''

import os
import sys
import components.metasploit as metasploit

def metasploitIt(ip_addr,port):
	
	
	print "[*] Trying enum shares on "+ ip_addr

	msf = metasploit.MSFController()
	msf.connect()
	msf.run('auxiliary/scanner/smb/enumshares', ip_addr, port,
			{"MaxDepth 1",})
	
	


def main(ip_addr, port):
	try:
		metasploitIt(ip_addr,port)
	except Exception as e:
		print e

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])
