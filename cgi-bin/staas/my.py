#!/usr/bin/python

print "Content-type:text/html\r\n\r\n"

import os,cgi,commands

x,y=commands.getstatusoutput("sudo mount -v /dev/mgrp/checkdr   /mnt/checkdr")
if x==0:
    print "Good"
else:
    print "Bad"

print y
