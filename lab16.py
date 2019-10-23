import requests
import json
import xlsxwriter

hostname = 'localhost'
url = 'http://%s:5000/json/cisco/routes' % hostname
username = 'student'
password = 'student'

data = requests.get(url, auth=(username, password))
format_data = data.content
json_output = json.loads(format_data)
workbook = xlsxwriter.Workbook('/home/student/Desktop/routes.xlsx')
worksheet = workbook.add_worksheet('router1')
worksheet.set_column(0,2,24)
row = 0
col = 0
for route in json_output['items']:
	dest_net = route['destination-network']
	dest_int = route['outgoing-interface']
	protocol = route['routing-protocol']
	worksheet.write(row, col, dest_net)
	worksheet.write(row, col + 1, dest_int)
	worksheet.write(row, col + 2, protocol)
	row += 1
	
workbook.close()
