import os
import re
import subprocess
import sys
import httplib
import threading
import pexpect
import uuid
from pexpect import EOF


class Scanner():
	def __init__(self, plugins, node):
		
		self.target_ports=[]
		self.triggers={}
		self.trigger_ports={}
		for plugin in plugins:
			for port in plugin.ports:
				if port not in self.target_ports:
					self.target_ports.append(str(port))

			if plugin.triggers[0] == '':
				for port in plugin.ports:

					self.trigger_ports[port]= plugin
			else:
				for trigger in plugin.triggers:
					self.triggers[trigger] = plugin

		self.node = node
	
	def _trigger(self, ip, port, scan_id):
	

		if port in self.trigger_ports:
			print "[+]", self.trigger_ports[port].name, "detected on", ip+":"+port
			self.node.command_run_plugin(self.trigger_ports[port].path, str(ip), str(port))
			return

		try:
			
			print "[*] Grabbing banner on "+ip+":"+port
			conn = httplib.HTTPConnection(ip, port, timeout=10)
			conn.request("GET","/")
			res = conn.getresponse()
			#print res.getheaders()
			#print str(res.read()).lower()
			head = str(res.getheaders()).lower()
			body = res.read().lower()

			last_trigger = ""

			for trigger in self.triggers: 
				if re.search(str(trigger).lower(), body) or re.search(str(trigger).lower(), head) :
					if last_trigger != trigger:
						if port in self.triggers[trigger].ports:
							last_trigger = self.triggers[trigger]
							print "[+]", last_trigger.name, "detected on", ip+":"+port
							self.node.command_run_plugin(last_trigger.path, str(ip), str(port), str(scan_id))
		except:  
			return  
	
	def launch(self):
		
		threads = []
		
		print "[*] ready to receive nmap or masscan command"
		print "[*] if not port selected, defaults one are :"

		#CREATE PORT LIST
		string_ports =""
		for port in self.target_ports:
			string_ports = string_ports+port+","
		string_ports=string_ports[:-1]
		print string_ports
		

		while True:
			last_input = raw_input ('>>>')
			if last_input == "exit":
				break
			elif last_input:
				m = re.match("(nmap|masscan) (?:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|localhost)(?:(\/\d{1,2})|(?:\s|$))", last_input)
				if m:
					if "nmap" in last_input:
						last_input += " -n --randomize-hosts -sS"

					if "nmap" in last_input and "-v" not in last_input:
						last_input = last_input + " -v"
						
					if "-p" not in last_input:
						last_input = last_input + " -p" + string_ports
					
					scan_id = str(uuid.uuid1())[:5]
					print "[+] launching scan "+scan_id+ " : "+ last_input
					child = pexpect.spawn (last_input)
					child.setecho(True)
					
					
					while child.isalive():
						try:
							child.expect('Discovered',timeout=None)
							line = child.readline().split()
							port_to_check = "".join("".join(line[-3]).split("/")[0])
							ip_to_check= "".join(line[-1:])
							print "[+] Open port on", ip_to_check +":"+port_to_check
							
							t = threading.Thread(	target=self._trigger, 
													args=(ip_to_check, port_to_check,scan_id))
							threads.append(t)
							t.start()
							
						except:
							break
					print "[*] ----- Scan Done ----- "
				
				else:
					print "[-] invalid command, format is \"nmap/masscan {ip} {parameters}\""
