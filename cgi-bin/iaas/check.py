#!/usr/bin/python
import cgi
import dbconnect
import json
sys.path.append("/var/www/cgi-bin/")
import encryptionkey
print "Content-Type: application/json\n\n"

#received user login form details
form_login=cgi.FieldStorage()
result={}
#taking username & password from form
username=form_login.getvalue('username').lower().strip()




result['status'] = 1
result['username'] = username
result['key'] = key


print json.dumps(result)
