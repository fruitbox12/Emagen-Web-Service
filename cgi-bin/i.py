#!/usr/bin/python

import cgi,os

print "Content-type: text/html\r\n\r\n"
print ""

#this is for recv data from cloud
data=cgi.FieldStorage()
os_name=data.getvalue('OSNAME')
os_ram=data.getvalue('RAMSIZE')
os_cpu=data.getvalue('CPUCORE')
os_hdd=data.getvalue('hdd')


if os_name == 'kali' :
	install3='sudo virt-install --graphics vnc,listen=192.168.10.151,port=5914  --cdrom /root/Desktop/kali.iso --ram '+os_ram+' --vcpu '+os_cpu+' --nodisk  --name '+os_name
	
	x=os.system(install3)
	if x!=0 :
		print "error"


print "okay"



