#!/usr/bin/python


import os,cgi,json

print "Content-Type: application/json\n\n"

formdata=cgi.FieldStorage()
result={}
#taking create atom form data
osname=formdata.getvalue("os")
grp=formdata.getvalue("grp")
atomname=formdata.getvalue("atomname")

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
	os.system('sudo qemu-img create -f qcow2 -b /var/lib/libvirt/images/generic.qcow2 /var/lib/libvirt/images/'+atomname+'.qcow2 ')
	install_os=os.system('sudo virt-install  --name '+atomname+' --ram '+ram+' --vcpu '+cpucore+' --disk path=/var/lib/libvirt/images/'+atomname+'.qcow2  --import  --graphics vnc,listen=192.168.122.1,port=5925,password=mypass')

if install_os!=0:
	result['status'] = 0
else:
	result['status'] = 1


print json.dumps(result)





