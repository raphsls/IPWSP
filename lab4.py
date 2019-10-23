import paramiko
import sys
import time
ip = '10.10.10.1'
enable = 'enable'
conf 'configure terminal'
shrun = 'show run'
termlength = 'terminal length 0'
DIR = '/home/student/Desktop/PYTHON/TEST/tst.txt'
username = 'cisco'
password1 = raw_input("Please provide the password to connect:\t")
password = 'cisco'

class REPLACE():
	def __init__(self, ipaddr):
		self.ipaddr = ipaddr
		self.DIR = DIR
		remote_conn_pre = paramiko.SSHClient()
		remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		remote_conn_pre.connect(self.ipaddr, username=username, password=password,
								look_for_keys=False, allow_agent=False)
		print "SSH connection established to %s" % self.ipaddr
		remote_conn = remote_conn_pre.invoke_shell()
		remote_conn.send(termlength + "\r")
		time.sleep(1)
		remote_conn.send(enable + "\r")
		remote_conn.send(password + "\r")
		remote_conn.send(shrun + "\r")
		time.sleep(5)

		output = remote_conn.recv(65534)
		self.output = output
		self.conn = remote_conn
	def Replace_IP(self):
		time.sleep(2)
		f = open(self.DIR, 'w')
		f.write(self.output.replace('192.168.12.1', '10.10.100.1'))
		f.close()
		
R1 = REPLACE(ip)
R1.Replace_IP()
