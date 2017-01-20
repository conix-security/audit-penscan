'''
plugin FTP
triggers=
ports=20,21
'''

import os
import sys
import ftplib


def tryingCreds(ip_addr,port):
	
	
	print "[*] Trying default FTP creds on "+ ip_addr

	f_users = open(os.path.dirname(os.path.realpath(__file__))+ "/wordlists/users", 'r')
	f_passwds = open(os.path.dirname(os.path.realpath(__file__))+ "/wordlists/pass", 'r')

	users = f_users.read()
	passwds = f_passwds.read()

	for user in (users).split('\n'):
		#user = user[:-1]
		for pwd in (passwds).split('\n'):
			#pwd =pwd[:-1]
			try:
				ftp = ftplib.FTP(ip_addr)
				ftp.login(user, pwd)
				print "[+] Creds found ! "+user+":"+pwd
				print "log Creds found ! "+user+":"+pwd
				ftp.quit()
			except:
				pass

	print "[*] Trying done."
	

def main(ip_addr, port):
	try:
		tryingCreds(ip_addr,port)
	except Exception as e:
		print e

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])
