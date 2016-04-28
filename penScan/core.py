
import os
import sys
import time
import ConfigParser

import penScan.scan.scanner as scan
import penScan.connection.node as connector

def main():
	try:

		#GET CONFIGS


		config = ConfigParser.ConfigParser()
		config.read("penScan/set.conf")

		ip_sploit = config.get('connection', 'ip_sploit')
		port_sploit = config.getint('connection', 'port_sploit')

		#CHECK TRIGGER/SPLOITER UP
		node = connector.node(port_sploit)
		if(not node.run_scan_node(ip_sploit)):
			if (not node.run_scan_node('localhost')):
				print "[-] no sploit node detected, launching one and trying locally"
				os.system("/usr/bin/gnome-terminal -e './start.py sploit'")
				time.sleep(1)


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
