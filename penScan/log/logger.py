import time
import os

def _followThePath(scan_id, ip, port, plugin_path):

	plugin_name = os.path.basename(os.path.splitext(plugin_path)[0])

	date = time.strftime("%d-%m")
	pwd = os.path.dirname((os.path.realpath(__file__)))

	nPath = pwd+"/"+date+"_"+scan_id
	if not os.path.exists(nPath):
		os.makedirs(nPath)

	nPath += "/"+ip
	if not os.path.exists(nPath):
		os.makedirs(nPath)

	return nPath, plugin_name

def logPluginEvent(scan_id, ip, port, plugin_path, event):
	
	nPath, plugin_name = _followThePath(scan_id,ip,port,plugin_path)

	nPath += "/"+plugin_name+"_"+port+".log"

	f = open(nPath, "w+")
	f.write(event+"\n")
	f.close()

def logDiscoveryEvent(scan_id, ip, port, plugin_path):

	nPath, plugin_name = _followThePath(scan_id,ip,port,plugin_path)

	nPath += "/Discoveries.log"

	f = open(nPath, "w+")
	f.write("Discovered "+plugin_name+" on "+ip+" "+port)
	f.close()