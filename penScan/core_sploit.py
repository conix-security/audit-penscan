
import ConfigParser

import penScan.connection.node as connector
import penScan.sploiter.plugins_controller as pController

def main(port_sploit=None):
	try:
		
		#GET CONFIGS
		if (port_sploit == None):
			config = ConfigParser.ConfigParser()
			config.read('penScan/set.conf')
			port_sploit = config.getint('connection', 'port_sploit')


		node = connector.node(int(port_sploit))
		node.run_sploit_node(pController)
		
		
	except Exception as e:
		print e