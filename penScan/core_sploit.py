
import ConfigParser

import penScan.connection.node as connector
import penScan.sploiter.plugins_controller as pController

def main():
	try:
		
		#GET CONFIGS
		config = ConfigParser.ConfigParser()
		config.read('penScan/set.conf')
		port_sploit = config.getint('connection', 'port_sploit')


		node = connector.node(port_sploit)
		node.run_sploit_node(pController)
		
		
	except Exception as e:
		print e