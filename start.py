#!/usr/bin/env python
import sys
import getopt

import penScan.core as core
import penScan.core_sploit as core_sploit

def run():

	try:
		opts, args = getopt.getopt(sys.argv[1:], "t:i:p:", ["type","ip","port"])
	except getopt.GetoptError as err:
		print str(err)  
		sys.exit(2)
	ip = None
	port = None
	aType = None
	for o, a in opts:
		if o in ("-i", "--ip"):
			ip = a
		elif o in ("-p", "--port"):
			port = a
		elif o in ("-t", "--type"):
			aType = a
		else:
			print "option not recognized"

	if aType == 'sploit':
			core_sploit.main(port)
	else:
		core.main(ip, port, aType)

if __name__ == "__main__":
	run()
