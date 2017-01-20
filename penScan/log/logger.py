
import time
import os

def getDirScan(scan_id):

	date = time.strftime("%d-%m")
	pwd = os.path.dirname((os.path.realpath(__file__)))

	nPath = pwd+"/"+date+"/"+scan_id
	if not os.path.exists(nPath):
		os.makedirs(nPath)

	return nPath

def _followThePath(scan_id, ip, port, plugin_path):

	nPath = getDirScan(scan_id)

	plugin_name = os.path.basename(os.path.splitext(plugin_path)[0])

	nPath += "/"+ip
	if not os.path.exists(nPath):
		os.makedirs(nPath)

	return nPath, plugin_name

def logPluginEvent(scan_id, ip, port, plugin_path, event):
	
	nPath, plugin_name = _followThePath(scan_id,ip,port,plugin_path)

	nPath += "/"+plugin_name+"_"+port+".log"

	f = open(nPath, "a+")
	f.write(event+"\n")
	f.close()

def logDiscoveryEvent(scan_id, ip, port, plugin_path):

	nPath, plugin_name = _followThePath(scan_id,ip,port,plugin_path)

	nPath += "/Discoveries.log"

	f = open(nPath, "a+")
	f.write("Discovered "+plugin_name+" on "+ip+" "+port+"\n")
	f.close()

def rcCreator(scan_id, ip, port, plugin_path, module, options=None):

	nPath, plugin_name = _followThePath(scan_id,ip,port,plugin_path)

	nPath += "/RCs/"+plugin_name+"_"+module+".rc"

	f = open(nPath, "w+")

	commands = """use """+module+"""
		set RHOST """+ip+"""
		set RHOSTS """+ip+"""
		set RPORT """+port
		
	#OPTIONS 
	if options:
		for option in options:
			commands = commands +"""
			set """+option

	commands = commands+"""
	exploit"""

	f.write(commands)
	f.close()