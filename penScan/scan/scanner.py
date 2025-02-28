import os
import re
import sys
import httplib
import threading
import pexpect
import uuid
from ..log import logger
from pexpect import EOF


class Scanner():
	def __init__(self, plugins, node):
		

		#self.target_ports=[80,443,8080,3306,1433...]
		#self.http_triggers{'Apache','Jboss',...}=Class_PLugin1,Class_Plugin2,...
		#self.ports_triggers{3306,1433...}=Class_PLugin1,Class_Plugin2,...

		self.target_ports=[]
		self.http_triggers={}
		self.ports_triggers={}
		self.string_ports=""
		for plugin in plugins:
			for port in plugin.ports:
				if port not in self.target_ports:
					self.target_ports.append(str(port))

			if plugin.triggers[0] == '':
				for port in plugin.ports:

					self.ports_triggers[port]= plugin
			else:
				for trigger in plugin.triggers:
					self.http_triggers[trigger] = plugin

		self.node = node
	
	def _trigger(self, ip, port, scan_id):
	
		final_test=True

		#Triggers on ports ONLY
		if port in self.ports_triggers:
			print "\033[32m[+] "+self.ports_triggers[port].name+" detected on "+ip+":"+port+'\033[0m'
			logger.logDiscoveryEvent(scan_id, ip, port, self.ports_triggers[port].path)
			self.node.command_run_plugin(self.ports_triggers[port].path, str(ip), str(port), str(scan_id))
			return

		#Triggers on http Keywords
		try:
			
			#print "[*] Grabbing banner on "+ip+":"+port
			conn = httplib.HTTPConnection(ip, port, timeout=10)
			conn.request("GET","/")
			res = conn.getresponse()
			#print res.getheaders()
			#print str(res.read()).lower()
			head = str(res.getheaders()).lower()
			body = res.read().lower()

			last_trigger = ""

			for trigger in self.http_triggers: 
				if re.search(str(trigger).lower(), body) or re.search(str(trigger).lower(), head) :
					if last_trigger != trigger:
						#if port in self.http_triggers[trigger].ports:
							last_trigger = self.http_triggers[trigger]
							print "\033[32m[+] "+last_trigger.name+" detected on "+ip+":"+port+'\033[0m'
							logger.logDiscoveryEvent(scan_id, ip, port, last_trigger.path)
							self.node.command_run_plugin(last_trigger.path, str(ip), str(port), str(scan_id))
							final_test=False
			if final_test:
				important_header = res.getheader('server')
				if important_header:
					print "[*] Header 'Server: "+important_header+"' found on "+ip+":"+port
				important_header = res.getheader('x-powered-by')
				if important_header:
					print "[*] Header 'X-Powered-By: "+important_header+"' found on "+ip+":"+port
		except:
			return
	
	def _execute_cmd(self, cmd):

		threads = []

		m = re.match("(nmap|masscan) (?:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|localhost|-iL .*)(?:(\/\d{1,2})|(?:\s|$))", cmd)
		if m:

			scan_id = str(uuid.uuid1())[:5]
			if "nmap" in cmd:
				cmd += " -n -sS"

			if "masscan" in cmd:
				cmd += " --interactive"

			if "nmap" in cmd and "-v" not in cmd:
				cmd += " -v"
				
			if "-p" not in cmd:
				cmd += " -p" + self.string_ports

			if "-oX" not in cmd:
				cmd += " -oX "+logger.getDirScan(scan_id)+"/output.xml"
			
			print "[+] launching scan "+'\033[31m'+scan_id+'\033[0m'+ " : "+ cmd
			child = pexpect.spawn (cmd)
			child.setecho(True)

			while child.isalive():
				try:
					child.expect('Discovered',timeout=None)
					line = child.readline().split()
					port_to_check = "".join("".join(line[-3]).split("/")[0])
					ip_to_check= "".join(line[-1:])
					print "[+] Open port "+port_to_check+" on "+ ip_to_check
					
					t = threading.Thread(	target=self._trigger, 
											args=(ip_to_check, port_to_check, scan_id))
					threads.append(t)
					t.start()


				except Exception as e:
					pass

			print "[*] ----- Scan Done ----- "
			try:
				self.node.receive_feedback()
			except:
				pass

		else:
			print "[-] invalid command, format is \"nmap/masscan {ip} {parameters}\""

	def launch(self):
		

		
		print "[*] ready to receive nmap or masscan command"
		print "[*] if no ports selected, defaults are :"

		#CREATE PORT LIST
		self.string_ports =""
		for port in self.target_ports:
			self.string_ports = self.string_ports+port+","
		self.string_ports=self.string_ports[:-1]
		print self.string_ports
		

		# stdscr = curses.initscr()

		# #curses.noecho()
		# #curses.echo()


		# begin_x = 
		# begin_y = 7
		# height = 1
		# width = 40
		# win = curses.newwin(height, width, begin_y, begin_x)
		# tb = curses.textpad.Textbox(win)
		# text = tb.edit()
		# curses.addstr(4,1,text.encode('utf_8'))

		# hw = "Hello world!"
		# while 1:
		# 	c = stdscr.getch()
		# 	if c == ord('p'): pass
		# 	elif c == ord('q'): break # Exit the while()
		# 	elif c == curses.KEY_HOME: x = y = 0

		# curses.endwin()


		#---------------------------CONSOLE---------------------
		class _Getch:
			def __init__(self):
				import tty, sys, termios # import termios now or else you'll get the Unix version on the Mac

			def __call__(self):	
				import sys, tty, termios
				fd = sys.stdin.fileno()
				old_settings = termios.tcgetattr(fd)
				try:
					tty.setraw(sys.stdin.fileno())
					ch = sys.stdin.read(1)
					if ch=="\x1b":
						ch+=sys.stdin.read(2)
						if ch[-1:].isdigit():
							ch+=sys.stdin.read(1)
				finally:
					termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
				return ch
		
		inkey = _Getch()
		
		prefix= ">>> "
		commands=[""]
		index=0
		pos=0
		while (True):
			command=""
			sys.stdout.write(prefix)
			index=len(commands)-1
			while(True):
				k=inkey()
				#print ord(k)
				if len(k)==1:
					if ord(k)==3: #Ctrl+C
						sys.stdout.write("\n")
						exit(0)
					elif ord(k)==13: #Enter
						sys.stdout.write("\n")
						command=command.lstrip()
						if command=='exit' or command=='quit':
							exit(0)
						elif command!=' ' and command:
							index=len(commands)-1
							commands[index]=command
							commands.append("")
							
							self._execute_cmd(command)
							pos=0
						break
					elif ord(k)==127: #BackSpace
						if pos>0:
							command=command[:pos-1]+command[pos:]
							sys.stdout.write("\x1b[2K\r"+prefix+command+"\b"*(len(command)-pos+1))
							pos-=1
					else:
						#sys.stdout.write(k+command[pos:]+"\b"*(len(command)-pos))
						command=command[:pos]+k+command[pos:]
						sys.stdout.write("\x1b[2K\r"+prefix+command+"\b"*(len(command)-pos-1))
						pos+=1
				elif len(k)==3:
					if k=='\x1b[A': #Arrow UP
						if index>0:
							commands[index]=command
							index-=1
							command = commands[index]
							sys.stdout.write("\x1b[2K\r"+prefix+command)
							pos=len(command)
					elif k=='\x1b[B': #Arrow DOWN
						if index<len(commands)-1:
							commands[index]=command
							index+=1
							command = commands[index]
							sys.stdout.write("\x1b[2K\r"+prefix+command)
							pos=len(command)
					elif k=='\x1b[C': #Arrow RIGHT
						if pos<len(command):
							sys.stdout.write(command[pos])
							pos+=1
					elif k=='\x1b[D': #Arrow LEFT
						if pos>0:
							sys.stdout.write("\b")
							pos-=1
				elif len(k)==4:
					if k=='\x1b[3~': #Delete
						command=command[:pos]+command[pos+1:]
						sys.stdout.write("\x1b[2K\r"+prefix+command+"\b"*(len(command)-pos))
		#---------------------------//////////---------------------

		# while True:
		# 	try:
		# 		cmd = raw_input ('>>>')
		# 		print cmd
		# 		if cmd == "exit":
		# 			break
		# 		elif cmd:
		# 			m = re.match("(nmap|masscan) (?:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|localhost)(?:(\/\d{1,2})|(?:\s|$))", cmd)
		# 			if m:
		# 				if "nmap" in cmd:
		# 					cmd += " -n --randomize-hosts -sS"

		# 				if "nmap" in cmd and "-v" not in cmd:
		# 					cmd += " -v"
							
		# 				if "-p" not in cmd:
		# 					cmd += " -p" + string_ports

		# 				if "-oX" not in cmd:
		# 					cmd += " -oX "+logger.getDirScan(scan_id)+"/output.xml"
						
		#				scan_id = str(uuid.uuid1())[:5]
		# 				print "[+] launching scan "+scan_id+ " : "+ cmd
		# 				child = pexpect.spawn (cmd)
		# 				child.setecho(True)
						
						
		# 				while child.isalive():
		# 					try:
		# 						child.expect('Discovered',timeout=None)
		# 						line = child.readline().split()
		# 						port_to_check = "".join("".join(line[-3]).split("/")[0])
		# 						ip_to_check= "".join(line[-1:])
		# 						print "[+] Open port on", ip_to_check +":"+port_to_check
								
		# 						t = threading.Thread(	target=self._trigger, 
		# 												args=(ip_to_check, port_to_check,scan_id))
		# 						threads.append(t)
		# 						t.start()


		# 					except:
		# 						break
		# 				print "[*] ----- Scan Done ----- "
					
		# 			else:
		# 				print "[-] invalid command, format is \"nmap/masscan {ip} {parameters}\""

		# 	except KeyboardInterrupt:
		# 		# quit
		# 		sys.exit()
