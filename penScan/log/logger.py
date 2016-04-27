import time
import os

def logEvent(scan_id, ip, port, plugin, event):
	
	date = time.strftime("%d-%m")
	pwd = os.path.dirname((os.path.realpath(__file__)))

	nPath = pwd+"/"+date+"_"+scan_id
	if not os.path.exists(nPath):
		os.makedirs(nPath)

	nPath += "/"+ip
	if not os.path.exists(nPath):
		os.makedirs(nPath)

	nPath += "/"+plugin+"_"+port

	f = open(nPath, "w+")
	f.write(event+"\n")
	f.close()