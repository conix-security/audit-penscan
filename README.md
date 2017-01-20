# penScan

## Initialisation

This tool needs two nodes to work; an exploit an a scan.  
The exploit node is a server listening on the port in penScan/set.conf, it can handle multiple connection.  
The scan node is a client connectiong to the host:port in penScan/set.conf  

At connection between two nodes, the client asks the server to send the list of its plugins.  
The server sends back every Python Plugins in the folder penScan/plugins/  
if you don't want a plugin to be used, remove it from the server plugins folder.  

If the option 'Split' does not launch the exploit node automatically, do :  
`./start.py -t exploit`  
`./start.py` in another shell.
  
## Scan

the client prompt awaits a valid nmap or masscan command, some examples of valid request are :  
`nmap 192.168.1.2`  
`masscan 165.23.0.0/16`  
`nmap -iL /path/to/listip -p 8080`  
...

the output will be stored in the log files.

At each discovered open ports, a command to the server will be send to run the plugins.  
Some plugins require metasploit to work. Metasploit should launch automatically. If not, in msfconsole, type :  
`load msgrpc Pass=msf`
  
## Usage

Usage : ./start.py [OPTIONS...]  
-t , --type		 Set the type of connection and interface  
	"exploit" : launch the exploit node  
	"local" : Exploit and scan nodes are both launched in the same terminal  
	"split" : Exploit and scan nodes are launched in different terminals  
	(without type, the scan node is launched and try to connect to an already running exploit node)  

-i , --ip  Use this ip instead of the set.conf file  
-p , --port Use this port instead of the set.conf file  



