'''
plugin JBoss
triggers=JBoss,WildFly,Undertow
ports=8080,9990
'''

import os
import sys
import httplib
import components.metasploit as metasploit


def metasploitIt(ip_addr,port):
	
	
	print "[*] Trying vuln scan jboss on "+ip_addr

	msf = metasploit.MSFController()
	msf.connect()
	msf.run('auxiliary/scanner/http/jboss_vulnscan', ip_addr, port)
	
def RCE_vuln_scan(ip_addr, port):
	#from /ressources/RCE_vuln_scan.py

	
	path = { "jmx-console"       : "/jmx-console/HtmlAdaptor?action=inspectMBean&name=jboss.system:type=ServerInfo",
			 "web-console"       : "/web-console/ServerInfo.jsp",
			 "JMXInvokerServlet" : "/invoker/JMXInvokerServlet"}
 
	for i in path.keys():
		try:
			print "[*] Checking %s: \t" %i
			conn = httplib.HTTPConnection(ip_addr, port)
			conn.request("HEAD", path[i])
			path[i] = conn.getresponse().status
			if path[i] == 200 or path[i] == 500:
				print "[+] [ VULNERABLE ]"
			else: print "[-] [ NOT VULNERABLE ]"
			conn.close()
		except:
			print "\n * An error ocurred while connecting"


def main(ip_addr, port):
	try:
		metasploitIt(ip_addr,port)
		RCE_vuln_scan(ip_addr,port)
	except Exception as e:
		print e

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])
