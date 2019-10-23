from paramiko import SSHClient,AutoAddPolicy
import time
import sys

ipaddr = '10.10.10.2'
username = 'cisco'
password = 'cisco'
enable = 'enable'
conf = 'configure terminal'
host = 'hostname R2'

def SSH_Connect():
	remote_conn_pre = SSHClient()
	remote_conn_pre.set_missing_host_key_policy(AutoAddPolicy())
	remote_conn_pre.connect(ipaddr, username=username, password=password,
							look_for_keys=False, allow_agent=False)
	remote_conn = remote_conn_pre.invoke_shell()
	print "Interactive SSH session established"
	output = remote_conn.recv(1000)
	print output
	remote_conn.send('terminal length 0\renable\rconf t')
	hostname = raw_input("Would would you like to change the hostname to: ")
	remote_conn.send("hostname {}\r".format(hostname))
	time.sleep(2)
	print "Hostname successfully changed {}".format(hostname)
	remote_conn_pre.close()

SSH_Connect()
sys.exit("operation completed")
