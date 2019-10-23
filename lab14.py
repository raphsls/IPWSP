import requests
from bs4 import BeautifulSoup

hostname = 'localhost'
url = 'http://%s:5000/xml/juniper/get-system-information' % hostname
username = 'student'
password = 'student'

get_data = requests.get(url, auth=(username, password))
data = get_data.text
soup = BeautifulSoup(data, 'lxml')

hostname = soup.find('host-name').string.strip()
firmware = soup.find('os-version').string.strip()
serial = soup.find('serial-number').string.strip()

print 'Hostname: %s' % hostname
print 'OS Version: %s' % firmware
print 'Serial Number: %s' % serial
