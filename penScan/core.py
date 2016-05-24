
import os
import sys
import time
import ConfigParser
import thread

import penScan.core_sploit as core_sploit
import penScan.scan.scanner as scan
import penScan.connection.node as connector

def main(ip_sploit=None, port_sploit=None, aType=None):
	try:

		#GET CONFIGS


		config = ConfigParser.ConfigParser()
		config.read("penScan/set.conf")

		if (ip_sploit == None):
			ip_sploit = config.get('connection', 'ip_sploit')
		if (port_sploit==None):
			port_sploit = config.getint('connection', 'port_sploit')


		

		node = connector.node(int(port_sploit))


		if aType==None:
			print "[*] connecting to "+str(ip_sploit)+":"+str(port_sploit)
			if(not node.run_scan_node(ip_sploit)):
				print "[-] Can't connect, aborting..."
				exit(0)

		elif aType=='split':

			os.system("/usr/bin/gnome-terminal -e './start.py -t sploit -p "+str(port_sploit)+"' &")
			time.sleep(1)

			if (not node.run_scan_node('localhost')):
				print "[-] Can't connect to local splited sploit node, aborting..."
				exit(0)

		elif aType=='local':

			thread.start_new_thread(core_sploit.main, (port_sploit,))

			if (not node.run_scan_node('localhost')):
				print "[-] Can't connect to local sploit node, aborting..."
				exit(0)

			
		#GET PLUGINS
		plugins = node.command_get_plugins()

		if plugins:
			print "[*] List of plugins loaded :"
			for plugin in plugins:
				print "[ ] " + plugin.path
		else:
			print "[-] No plugins loaded"
			exit(0)

		#LAUNCH CONSOLE
		s = scan.Scanner(plugins, node)
		s.launch()
		
	except Exception as e:
		print e
