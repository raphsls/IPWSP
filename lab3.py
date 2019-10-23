import paramiko
import sys
import time
import getpass

ip1 = "10.10.10.1"
ip2 = "10.10.10.2"
ip3 = "10.10.10.3"
ip4 = "10.10.10.4"

ip_list = [ip1,ip2,ip3,ip4]

enable = "enable"
conf = "configure terminal"
termlength = "terminal length 0"
password = getpass.getpass()
username = "cisco"

def Session1(name, ipaddr):
	remote_conn_pre = paramiko.SSHClient()
	remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	remote_conn_pre.connect(ipaddr, username=username, password=password,
							look_for_keys=False, allow_agent=False)
	print "SSH connection established to %s" % ipaddr
	remote_conn = remote_conn_pre.invoke_shell()

	remote_conn.send(termlength + "\r")
	remote_conn.send(enable + "\r")
	remote_conn.send(password + "\r")
	time.sleep(5)
	remote_conn.send(conf + "\r")
	time.sleep(1)
	remote_conn.send(name + "\r")
	time.sleep(1)
	output = remote_conn.recv(1000)
	print output
	remote_conn_pre.close()

for ip in ip_list:
	Session1('hostname R{}'.format(ip[-1]), ip)

sys.exit("operation completed")
