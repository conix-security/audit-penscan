#!/usr/bin/env python
import sys
import getopt

import penScan.core as core
import penScan.core_sploit as core_sploit

def run():

	try:
		opts, args = getopt.getopt(sys.argv[1:], "t:i:p:h", ["type","ip","port","help"])
	except getopt.GetoptError as err:
		print str(err)  
		sys.exit(2)
	ip = None
	port = None
	aType = None
	for o, a in opts:
		if o in ("-h", "--help"):
			print "Usage : ./start.py [OPTIONS...]\n"
			print "-t , --type \t Set the type of connection and interface"
			print "\t \"exploit\" : launch the exploit node"
			print "\t \"local\" : Exploit and scan nodes are both launched in the same terminal"
			print "\t \"split\" : Exploit and scan nodes are launched in different terminals"
			print "(without type, the scan node is launched and try to connect to an already running exploit node)\n"
			print "-i , --ip \t Use this ip instead of the set.conf file"
			print "-p , --port \t Use this port instead of the set.conf file"
			exit(0)

		elif o in ("-i", "--ip"):
			ip = a
		elif o in ("-p", "--port"):
			port = a
		elif o in ("-t", "--type"):
			aType = a
		else:
			print "option not recognized"

	if aType == 'exploit':
			core_sploit.main(port)
	else:
		core.main(ip, port, aType)

if __name__ == "__main__":
	run()
