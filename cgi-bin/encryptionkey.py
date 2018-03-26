#!usr/bin/python

def encryptuser(username):
        key='K'
	encrypted=""
	a=list(username)
	b=list(username)
        for i in a:
            i = chr(ord(i)^ord(key))
	index=0
        for i in a:
            w=0
            for j in a:
                if i==j:
                    w=w+1

            for j in range(index,len(a)):
            	w+=ord(a[j])
            
            w = 33 + w%93
            b[index] = chr(w)

	    index+=1

        encrypted = "".join(b)
        return encrypted


