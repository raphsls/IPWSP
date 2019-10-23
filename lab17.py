import requests
import sqlite3 as sql
import sys
import json
from bs4 import BeautifulSoup

hostname = 'localhost'
json_url = 'http://%s:5000/json/contacts' % hostname
xml_url = 'http://%s:5000/xml/contacts' % hostname
username = 'student'
password = 'student'
db_name = '/home/student/ipwsp/databases/ipwsp.db'
url_list = [json_url, xml_url]
conn = sql.connect(db_name)
curs = conn.cursor()

def TableCreate(url):
    if 'json' in url:
        table = 'json_contacts'
    elif 'xml' in url:
        table = 'xml_contacts'
    
    print '- Creating/flushing database table %s' % table
    try:
        curs.execute("CREATE TABLE %s (id text, first text, last text,\
                      gender text, email text, ip text)" % table)
    except:
        conn.rollback()
        curs.execute("DROP TABLE %s" % table)
        curs.execute("CREATE TABLE %s (id text, first text, last text,\
                      gender text, email text, ip text)" % table)

def RestToDB(url):
    print '-Making RESTful Call to Endpoint'
    get_data = requests.get(url, auth=(username, password))
    if 'json' in url:
        table = 'json_contacts'
        data = get_data.content
        json_output = json.loads(data)
        print '- Iterating JSON Data and inserting into database'
        for contact in json_output['items']:
            contact_id = contact['id']
            first_name = contact['first_name']
            last_name = contact['last_name']
            gender = contact['gender']
            email = contact['email']
            ip_addr = contact['ip_address']
            curs.execute("INSERT INTO %s VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"\
                         % (table, contact_id, first_name, last_name, gender, email, ip_addr))
                         
    elif 'xml' in url:
        table = 'xml_contacts'
        data = get_data.text
        soup = BeautifulSoup(data, 'lxml')
        print '- Iterating XML Data and inserting into database'
        for i in soup.find_all('record'):
            contact_id = i.find('id').string.strip()
            first_name = i.find('first_name').string.strip()
            last_name = i.find('last_name').string.strip()
            gender = i.find('gender').string.strip()
            email = i.find('email').string.strip()
            ip_addr = i.find('ip_address').string.strip()
            curs.execute("INSERT INTO %s VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"\
                         % (table, contact_id, first_name, last_name, gender, email, ip_addr))
for url in url_list:
    TableCreate(url)
    RestToDB(url)
    conn.commit()
conn.close()
