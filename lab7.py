import paramiko
import time
import sys

term = 'terminal length 0\r'
priv_mode = "en\rcisco\r"
global_mode = 'conf t\r'
username = 'cisco'
password = 'cisco'

class IOSConnect():
    def __init__(self, ipaddr):
        try:
            self.ssh_prep = paramiko.SSHClient()
            self.ssh_prep.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_prep.connect(ipaddr, username=username, password=password,
                             look_for_keys=False, allow_agent=False)
        except IOError:
            sys.exit("Failed to connect")
        else:
            print "Connection established on {}".format(ipaddr)
            self.conn = self.ssh_prep.invoke_shell()
            self.conn.send(term)
            self.conn.send(priv_mode)

    def get_version(self):
        self.conn.send('show ver\r')
        time.sleep(3)
        self.output = self.conn.recv(65543)
        print self.output

    def get_inv(self):
        self.remote_conn.send('sh inv\r')
        time.sleep(2)
        self.output = self.remote_conn.recv(65534)
        print "Attempting to get the Serial Number of the Appliance!"
        serial = re.search(r'SN:\s(.*?)\r', self.output)
        print "The Serial number is:\t\t{}\n".format(serial.group(1))

    def get_log(self):
        self.remote_conn.send('show log\r')
        time.sleep(3)
        self.output = self.remote_conn.recv(65534)
        print "Acquiring Logging Info!"
        logs = re.findall(r'.*IPACCESSLOGDP.*', self.output)
        if logs:
            print "There is/are {} deny entries on the access-list PYTHON\n".format(len(logs))
        else:
            print "No entries found"
        if len(logs) > 0:
            answer = raw_input("Would you like to view these errors? (y/n) ")
            if answer == "y":
                for entry in logs:
                    print entry
            else:
                print "Until next time!"

def pinger(ip):
    remote_conn_pre = paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_conn_pre.connect(ip, username="cisco", password="cisco",
                            look_for_keys=False, allow_agent=False)
    remote_conn = remote_conn_pre.invoke_shell()
    print "{} is ready".format(ip)
    ping1 = raw_input("ping ")
    remote_conn.send('ping {}\r'.format(ping1))
    time.sleep(4)
    output = remote_conn.recv(10000)
    print output
    ping2 = raw_input("ping ")
    remote_conn.send('ping {}\r'.format(ping2))
    time.sleep(4)
    output = remote_conn.recv(10000)
    print output

pinger("10.10.10.2")


R1 = IOSConnect('10.10.10.1')
R1.get_version()
