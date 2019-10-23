import paramiko
import sys
import time

enable = 'enable'
disable = 'disable'
conf = 'configure terminal'
shrun = 'show run'
termlength = 'terminal length 0'
username = 'cisco'
password = 'cisco'

filelist = open('/home/student/Desktop/PYTHON/Python-Scripts/MPLS3.txt')

class Session(object):

    def SSHConnect(self, ip):
        self.ip = ip
        try:
            ssh_prep = paramiko.SSHClient()
            ssh_prep.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_prep.connect(self.ip, username=username, password=password,
                             look_for_keys=False, allow_agent=False)
        except IOError:
            sys.exit("Failed to connect...")
        else:
            print "SSH connection established to {}".format(self.ip)
            conn = ssh_prep.invoke_shell()
            conn.send('term length 0\ren\rcisco\rsh run\r')
            time.sleep(5)
            output = conn.recv(65543)
            return output

    def Postrun(self, filename, run_cfg):
        HOME = "/home/student/Desktop/PYTHON/TEST/Routers-2/%s" % (filename)
        f = open(HOME.strip(), 'w')
        f.write(run_cfg)
        f.close()

ssh = Session() # This reprsesnts the class

runfiles = []

y = 1
while y != 5:
    if y < 5:
        print "\nGetting Running Config for R%s" % y
        run = ssh.SSHConnect("10.10.10.%s" % y)
        y += 1
        runfiles.append(run)
    else:
        print "\nGetting Running Config for R%s" % y
        runfiles.append(run)
        y += 1

for each_filename, each_shrun in zip(filelist, runfiles):
    ssh.Postrun(each_filename, each_shrun)
sys.exit("operation completed")
