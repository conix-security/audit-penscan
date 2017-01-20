'''
plugin NFS
triggers=
ports=111
'''


import sys
import components.metasploit as metasploit

def metasploitIt(ip_addr,port):
	
	
	print "[*] Trying NFS mounts scan on "+ ip_addr

	msf = metasploit.MSFController()
	msf.connect()
	msf.run('auxiliary/scanner/nfs/nfsmount', ip_addr, port,)
	
	


def main(ip_addr, port):
	try:
		metasploitIt(ip_addr,port)
	except Exception as e:
		print e

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])
