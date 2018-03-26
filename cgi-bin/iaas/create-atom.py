#!/usr/bin/python

import cgi,json,commands,os,time,pyqrcode
from random import randint
import mysql.connector as mariadb


print "Content-Type: application/json\n\n"

mariadb_connection = mariadb.connect(user='root', password='dbpass', database='mol')
cursor = mariadb_connection.cursor()

formdata=cgi.FieldStorage()
result={}
#taking create atom form data
osname=formdata.getvalue("os")
grp=formdata.getvalue("grp")
atomname=formdata.getvalue("atomname")
username="tej1996"

#setting values for each group
if grp=="grp1":
	ram="256"
	cpucore="1"
	hdd="1"
elif grp=="grp2":
	ram="1024"
	cpucore="1"
	hdd="2"
elif grp=="grp3":
	ram="1024"
	cpucore="2"
	hdd="5"
elif grp=="grp4":
	ram="1024"
	cpucore="2"
	hdd="10"	


if osname=="ubuntu":
	baseosname="generic"
elif osname=="centos":
	baseosname="centosbase"
elif osname=="redhat":
	baseosname="redhatbase"
elif osname=="kali":
	baseosname="kalibase"
elif osname=="windows":
	baseosname="winbase"

try:
	#checking if atomname exists or not
	cursor.execute("SELECT atomname from users_iaas WHERE atomname=%s", (atomname,))
	rows_atom = cursor.fetchall()
	num_rows_atom = cursor.rowcount

	#retrieving the userid of current user
	cursor.execute("SELECT id from users WHERE username=%s",(username,))
	rows_userid = cursor.fetchall()
	num_rows_userid = cursor.rowcount
	#setting flag for available port	
	avail=False
	#checking for port if available or not,if not generate new and check again
	while avail == False:
		websockify_port = randint(6000, 6800)
		vnc_port = randint(5900, 5999)

		# retrieving the vnc_port & websockify_port from db
		cursor.execute("SELECT vnc_port,websockify_port from users_iaas WHERE vnc_port=%s || websockify_port=%s", (vnc_port,websockify_port))
		rows_ports = cursor.fetchall()
		num_rows_ports = cursor.rowcount

		#checking the specified port already binded or not
		web_port_status,web_port_out=commands.getstatusoutput("netstat -nltu | grep "+str(websockify_port))
		vnc_port_status,vnc_port_out=commands.getstatusoutput("netstat -nltu | grep "+str(vnc_port))

		if num_rows_ports==0:
			if web_port_status!=0 and vnc_port_status!=0:
				avail=True

	if num_rows_userid == 1:

		if num_rows_atom == 0:

			#install os with virt-install
			commands.getstatusoutput('sudo qemu-img create -f qcow2 -b /var/lib/libvirt/images/'+baseosname+'.qcow2 /var/lib/libvirt/images/' + atomname + '.qcow2')

			ins_status,install_os = commands.getstatusoutput('sudo virt-install  --name ' + atomname + ' --ram ' + ram + ' --vcpu ' + cpucore + ' --disk path=/var/lib/libvirt/images/' + atomname + '.qcow2  --import  --graphics vnc,listen=192.168.122.1,port='+str(vnc_port)+' --noautoconsole')
			time.sleep(30)
			machine_ip=commands.getoutput("sudo virsh domifaddr "+atomname+" | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'")
			novnc_url="http://192.168.122.1:"+str(websockify_port)
			if ins_status == 0:
				# insert created atom entry into users_iaas table
				try:
					run_status="active"
					cursor.execute("INSERT into users_iaas(uid,atomname,osname,grpname,vnc_port,websockify_port,machine_ip,novnc_url,status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (rows_userid[0][0],atomname,osname,grp,vnc_port,websockify_port,machine_ip,novnc_url,run_status))
					mariadb_connection.commit()
					mariadb_connection.close()
					os.system('sudo websockify --web=/usr/share/novnc '+str(websockify_port)+' 192.168.122.1:'+str(vnc_port)+' -D')
					qrcode=pyqrcode.create(novnc_url)
					qrcode.png("/var/www/html/molecular/iaas/qrcodes/"+atomname+".png",scale=8)
					result['status'] = 1
				except:
					result['status'] = "Unable to store to database!"
			else:
				result['status'] =  2
		else:
			result['status'] = 3
	else:
		result['status'] = "User does not exist!"
except mariadb.Error as err:
		result['status']=format(err)

print json.dumps(result)





