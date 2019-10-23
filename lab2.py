from paramiko import SSHClient, AutoAddPolicy
import time
import sys

def Hostname_Updater(ipaddr, username='cisco', password='cisco'):
	remote_conn_pre = SSHClient()
	remote_conn_pre.set_missing_host_key_policy(AutoAddPolicy())
	remote_conn_pre.connect(ipaddr, username=username, password=password,
							look_for_keys=False, allow_agent=False)
	print "...Connection established on {}...".format(ipaddr)
	remote_conn = remote_conn_pre.invoke_shell()
	output = remote_conn.recv(1000)
	print output
	remote_conn.send("terminal length 0\renable\rcisco\rconf t\r")
	hostname = raw_input("New hostname: ")
	time.sleep(0.5)
	remote_conn.send("hostname {}\r".format(hostname))
	print "Hostname successfully updated to {}".format(hostname)
	remote_conn_pre.close()

R1 = Hostname_Updater('10.10.10.1')
R2 = Hostname_Updater('10.10.10.2')
R3 = Hostname_Updater('10.10.10.3')
R4 = Hostname_Updater('10.10.10.4')
sys.exit()
	
