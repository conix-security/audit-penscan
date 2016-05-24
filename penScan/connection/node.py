
import socket
import threading
import json
import pickle

class node():
	def __init__(self, port):
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
#------------------------------------------------------------------------------------
	
	#SCAN
	def run_scan_node(self, ip):
		
		self.sock.settimeout(5)
		try:
			self.sock.connect((ip, self.port))
			return 1
		except:
			return 0
	
	#SCAN
	def command_run_plugin(self, path, ip, port, scan_id):
		msg = "RUN "+path+" "+ip+" "+port+" "+scan_id
		try:
			sent = self.sock.send(msg)
		except:
			print "[-] Error while sending command RUN"
	#SCAN
	def command_get_plugins(self):
		msg = "GET PLUGINS"
		try:
			sent = self.sock.send(msg)
			plugins = self.sock.recv(10000)
			return pickle.loads(plugins)
		except:
			print "[-] Error while sending command GET"

#------------------------------------------------------------------------------------

	#SPLOIT
	def run_sploit_node(self, pController):

		self.pController = pController

		self.sock.bind(('', self.port))
		self.sock.listen(10)
		print '[*] Exploit node listening'

		while True:

			conn, addr = self.sock.accept()
			print '[+] Connected with ' + addr[0] + ':' + str(addr[1])
			
			t = threading.Thread(target=self._clientthread, args=(conn,))
			t.start()
			
			
		self.sock.close()
	
	#SPLOIT
	def _clientthread(self, conn):

		while True:
			data = conn.recv(1024)
			if data:
				keywords = data.split()
				print keywords
				first_word = str(keywords[0])

				if  str(keywords[0]) == 'RUN':

					t = threading.Thread(	target=self.pController.run, 	
											args=(	str(keywords[1]), 
													str(keywords[2]), 
													str(keywords[3]),
													str(keywords[4]))
										)
					t.start()

				elif str(keywords[0]) == 'GET':

					plugins = self.pController.get_plugins()
					str_plugins = pickle.dumps(plugins)
					conn.send(str_plugins)
			else:
				conn.shutdown(2)
				conn.close()
				break
