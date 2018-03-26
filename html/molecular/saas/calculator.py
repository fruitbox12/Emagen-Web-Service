#!/usr/bin/python

import getpass, socket,time, sys,os

sock= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
SERVER_IP="192.168.122.152"
SERVER_PORT=8000

#client's username & password
#username=sys.argv[1]
#password=sys.argv[2]


#os.system("sshpass -p "+password+" ssh -X "+username+"@"+SERVER_IP+" gnome-calculator")

os.system("sshpass -p 123 ssh -X test@"+SERVER_IP+" gnome-calculator")

#execfile('client/saas.py')
