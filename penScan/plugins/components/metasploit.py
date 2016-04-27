import msfrpc
import string
import time
import msgpack
import httplib




class MSFController():

	def __init__(self):
		
		self.uri = "/api/"
		self.headers = {"Content-type" : "binary/message-pack" }
		self.token = None

	def _call(self,meth,opts = []):


		if self.token:
			opts.insert(0,self.token)

		opts.insert(0,meth)
		params = msgpack.packb(opts)
		self.client.request("POST",self.uri,params,self.headers)
		resp = self.client.getresponse()
		return msgpack.unpackb(resp.read()) 

	def _login(self,user,password):
		ret = self._call('auth.login',[user,password])
		if ret.get('result') == 'success':
			self.token = ret.get('token')

  

	def connect(self, host='127.0.0.1', port=55552):
		
		self.client = httplib.HTTPConnection(host,port)

		self._login('msf','msf')
		ress = self._call('console.create')
		self.console_id = ress['id']
		
	def run(self, module, target, port, options=None):
		
		commands = """use """+module+"""
		set RHOST """+target+"""
		set RHOSTS """+target+"""
		set RPORT """+port
		
		#OPTIONS 
		if options:
			for option in options:
				commands = commands +"""
				set """+option

		commands = commands+"""
		exploit
		"""

		self._call('console.write',[self.console_id,commands])

		while True:
			res = self._call('console.read',[self.console_id])        
			if len(res['data']) > 1:
				for line in string.split(res['data'], '\n'):
					if line.startswith('[+]'):
						print "log", line
					print line
					if "completed" in line:
						return
						#self._call('console.destroy',[self.console_id])
				continue
			if res['busy'] == True:             
				time.sleep(1)  