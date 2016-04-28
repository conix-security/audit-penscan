import os
import re
import sys
from subprocess import PIPE, Popen
from ..log import logger 

class plugin:
	def __init__(self, name, path, triggers, ports):
		self.name=name
		self.path=path
		self.triggers=triggers
		self.ports=ports

def get_plugins():

	plugins_path = os.path.dirname(os.path.dirname((os.path.realpath(__file__))))+"/plugins"

	print "[*] loading python plugins from directory", plugins_path
	
	plugins = []
	
	for filename in os.listdir(plugins_path):
		path = plugins_path+"/"+filename
		try:
			f = open(path, 'r')
			m = re.search("plugin (?P<name>.*)\ntriggers=(?P<triggs>.*)\nports=(?P<ports>.*)\n", f.read())
			if m:
				new_plugin = plugin(m.group('name'), path, m.group('triggs').split(','), m.group('ports').split(','))
				plugins.append(new_plugin)
		except:
			pass
			
	return plugins


def run(path, ip ,port, id):

	line = "not empty"

	print "[*] launching "+ path

	p = Popen([sys.executable, path, ip, port],stdin=PIPE,stdout=PIPE)
	while (p.poll() == None) or (line != ''):
		line = p.stdout.readline()
		line = line[:-1]
		if line.startswith('[+]'):
			print '\033[32m'+line #green
		elif line.startswith('[*]'):
			print '\033[0m'+line #white
		elif line.startswith('[-]'):
			print '\033[31m'+line #red
		elif line.startswith('log'):
			logger.logPluginEvent(id, ip, port, plugin_path, line[4:])
