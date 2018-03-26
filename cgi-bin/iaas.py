#!/usr/bin/python


import os,cgi

print "Content-Type: text/html\r\n\r\n"
print ""


formdata=cgi.FieldStorage()


osram=formdata.getvalue("osram")
oscpu=formdata.getvalue("oscpu")
osname=formdata.getvalue("osname")
osdisk=formdata.getvalue("osdisk")


install_os=os.system('sudo virt-install --graphics vnc,listen=192.168.122.1,port=1233 --cdrom /root/Downloads/kalilinux.iso --ram '+osram+' --vcpu '+oscpu+' --nodisk --name '+osname)

if install_os!=0:
	print "Error"
else:	
	print "Done"
