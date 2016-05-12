'''
plugin MsSQL
triggers=
ports=1433
'''

import os
import sys
import httplib, urllib
import components.metasploit as metasploit

def metasploitIt(ip_addr,port):
	
	
	print "[*] Trying default pass on "+ ip_addr

	msf = metasploit.MSFController()
	msf.connect()
	msf.run('auxiliary/scanner/mssql/mssql_login', ip_addr, port, 
			{"PASS_FILE "+os.path.dirname(os.path.realpath(__file__))+"/wordlists/pass",
			"USER_FILE "+os.path.dirname(os.path.realpath(__file__))+"/wordlists/users"})
	


def main(ip_addr, port):
	try:
		metasploitIt(ip_addr,port)
	except Exception as e:
		print e

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])