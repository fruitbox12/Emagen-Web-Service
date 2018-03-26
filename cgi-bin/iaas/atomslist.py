#!/usr/bin/python

import cgi,json,commands,os
from random import randint
import mysql.connector as mariadb


print "Content-Type: application/json\n\n"

mariadb_connection = mariadb.connect(user='root', password='dbpass', database='mol')
cursor = mariadb_connection.cursor()

formdata=cgi.FieldStorage()
result={}
#taking create atom form data
username="tej1996"
try:
	#retrieving the userid of current user
	cursor.execute("SELECT id from users WHERE username=%s",(username,))
	rows_userid = cursor.fetchall()
	num_rows_userid = cursor.rowcount
	
	if num_rows_userid == 1:
		
		try:
			cursor.execute("SELECT osname,atomname,machine_ip,novnc_url,status,aid from users_iaas WHERE uid=%s",(rows_userid[0][0],))
			rows = cursor.fetchall()
			num_rows_atoms = cursor.rowcount

			if num_rows_atoms!=0:
				result['data']=rows
			else:
				result['data']=""
			mariadb_connection.commit()
			mariadb_connection.close()
			result['status'] = 1
		except:
			result['status']=format(mariadb.Error)
	else:
		result['status'] = 0
except mariadb.Error:
		result['status']=format(mariadb.Error)

print json.dumps(result)





