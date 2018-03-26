#!/usr/bin/python

import cgi,json,commands,os,time,sys, pyqrcode
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import dbconnect
from random import randint


print "Content-Type: application/json\n\n"

formdata=cgi.FieldStorage()
result={}
#taking atom action data
aid=formdata.getvalue("aid")
action=formdata.getvalue("action")
username=formdata.getvalue("username")


try:

    # retrieving the userid of current user
    dbconnect.cursor.execute("SELECT id from users WHERE username=%s", (username,))
    rows_userid = dbconnect.cursor.fetchall()
    num_rows_userid = dbconnect.cursor.rowcount

    if num_rows_userid == 1:

        try:
            #checking if atomname exists or not
            dbconnect.cursor.execute("SELECT atomname,websockify_port from users_iaas WHERE aid=%s", (aid,))
            rows_atom = dbconnect.cursor.fetchall()
            num_rows_atom = dbconnect.cursor.rowcount

            atomname=rows_atom[0][0]
            websockify_port=rows_atom[0][1]

            if num_rows_atom==1:
                #performing action on atom

                if action=="reboot":
                    r_status,r_out=commands.getstatusoutput("sudo virsh reboot "+atomname)
                    if r_status==0:
                        dbconnect.cursor.execute("UPDATE users_iaas SET status=%s WHERE aid=%s",
                                                 ("active", aid))
			result['status']=1
                    else:
                        result['status']="Unable to perform your action, Sorry!"

                if action=="power":
                    dbconnect.cursor.execute("SELECT status from users_iaas WHERE aid=%s", (aid,))
                    row = dbconnect.cursor.fetchall()
                    if row[0][0]=="active":
                        commands.getstatusoutput("sudo virsh shutdown " + atomname)
                        dbconnect.cursor.execute("UPDATE users_iaas SET status=%s WHERE aid=%s",
                                             ("inactive", aid))
                    if row[0][0]=="inactive":
                        commands.getstatusoutput("sudo virsh start "+atomname)
                        dbconnect.cursor.execute("UPDATE users_iaas SET status=%s WHERE aid=%s",
                                                 ("active", aid))
                    result['status'] = 1

                if action=="delete":
		    a_status,a_out = commands.getstatusoutput("sudo virsh list --inactive | grep -w "+atomname+" | awk '{print $3}'")
                    if a_out!="shut":
			p_status, p_out = commands.getstatusoutput("sudo virsh shutdown " + atomname)
                    else:
			p_status=0
		    if p_status==0:
                        commands.getstatusoutput("sudo virsh undefine "+atomname)
                        commands.getstatusoutput("sudo rm -rf /var/lib/libvirt/images/"+atomname+".qcow2")
                        ps,pid=commands.getstatusoutput("sudo lsof -n -i :"+str(websockify_port)+" |grep LISTEN | awk '{print $2}'")
                        commands.getstatusoutput("sudo kill -9 "+str(pid))
                        dbconnect.cursor.execute("DELETE from users_iaas WHERE aid=%s",(aid,))
			commands.getstatusoutput("sudo rm -rf /var/www/html/molecular/iaas/qrcodes/"+atomname+".png")
			result['status']=1
                    else:
                        result['status'] = "Unable to perform your action, Sorry!"

            dbconnect.mariadb_connection.commit()
            dbconnect.mariadb_connection.close()
        except Exception as err:
            result['status']=format(err)
    else:
        result['status'] = 0

except Exception as err:
        result['status']=format(err)

print json.dumps(result)





