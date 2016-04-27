'''
plugin Tomcat
triggers=Apache-Coyote
ports=8080,80,443,8081,8000,8008,8443,8444,8880,8888,9080,19300
'''

import os
import sys
import components.metasploit as metasploit

def metasploitIt(ip_addr,port):
	
	
	print "[*] Trying default pass on "+ ip_addr

	msf = metasploit.MSFController()
	msf.connect()
	msf.run('auxiliary/scanner/http/tomcat_mgr_login', ip_addr, port)
	
	


def main(ip_addr, port):
	try:
		metasploitIt(ip_addr,port)
	except Exception as e:
		print e

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])
