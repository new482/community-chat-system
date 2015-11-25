#!/usr/bin/env python
import socket
import sys
import select
import os
import string
import struct
import time
import fcntl
import thread
from datetime import datetime as dt

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 8888
addressInNetwork = []

send_address = (MCAST_GRP, MCAST_PORT) # Set the address to send to
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # Create Datagram Socket (UDP)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Make Socket Reusable
s.setblocking(False) # Set socket to non-blocking mode
s.bind((MCAST_GRP, MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

print "Accepting connections on port", hex(MCAST_PORT)

def getLine():
    inputReady,outputReady,exceptionReady = select.select([sys.stdin],[],[],0.0001)
    for socketSelect in inputReady:
        if socketSelect == sys.stdin:
            input = sys.stdin.readline()
            return input    
    return False

def checkBug(checkRoom):
    flag = False    
    try:
        roomNumber = int(checkRoom)
        if (roomNumber==1) or (roomNumber==2) or (roomNumber==3) or (roomNumber==4):
            flag = True
    except:
        pass   
    return flag

def getip(name):
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    return socket.inet_ntoa(
       fcntl.ioctl(
         s.fileno(),
         0x8915,
         struct.pack('256s',name[:15])
       )[20:24]
    )

def sendRequestFiles():
    print "REQUEST FILES"
    s.sendto("ASK-FILE", send_address)

def mergefile(file, fileName):
    masterContent = ""
    someOneContent = file.split("\n")
    myfile = open(fileName, 'r')
    myfile = myfile.read()
    myContent = myfile.split("\n")
    for index1 in range(len(myContent)):
        if myContent[index1]:
                masterContent += myContent[index1] + "\n"
    for index2 in range(len(someOneContent)):
        if someOneContent[index2] not in masterContent:
                if someOneContent[index2]:
                        masterContent += someOneContent[index2] + "\n"

    sortBydate(masterContent,fileName)
    myfile.close()

def mergeuserfile(file, filename):
	if "***@user" in file:
		container = file.split("***@user")
		file = container[1]

	masteruser = ""
	updatinguser = file.split("\n")
	myuserfile = open(filename, 'r')
	myuserfile = myuserfile.read()
	checkuserfile = myuserfile.split("\n")
	for index1 in range(len(checkuserfile)):
        	if checkuserfile[index1]:
                	masteruser += checkuserfile[index1] + "\n"
	for index2 in range(len(updatinguser)):
	        if updatinguser[index2] not in masteruser:
	                if updatinguser[index2]:
	                        masteruser += updatinguser[index2] + "\n"
	
	writefile = open(filename,'w')
	writefile.write(masteruser)
	writefile.close()

def sortBydate(file,fileName):
    masterSorted = ""
    splitLine  = file.split('\n')
    spliterSize = len(splitLine) - 1

    for outline in range(spliterSize):
        outdate = dt.strptime('Mon Jan 01 00:00:00 3000', "%a %b %d %H:%M:%S %Y")
        outString = ""
        for inline in range(spliterSize):
                inspliteLine = splitLine[inline].split('|')
                indateTemp   = inspliteLine[2]
                indate       = dt.strptime(indateTemp, "%a %b %d %H:%M:%S %Y")

                if splitLine[inline] not in masterSorted:
                        if outdate > indate :
                                outdate = indate
                                outString = splitLine[inline]

        masterSorted += outString + "\n"

    writefile = open(fileName, 'w')
    writefile.write(masterSorted)
    writefile.close()

def callThread():
    #start thread dispatch
    thread.start_new_thread(dispatch, ())
   
def dispatch():
    time.sleep(86400) #delete history every 24 hours
    deleteHistory()

def deleteHistory():
    f1 = open('log1.txt', 'w')
    f1.write("")
    f1.close()
    
    f2 = open('log2.txt', 'w')
    f2.write("")
    f2.close()

    f3 = open('log3.txt', 'w')
    f3.write("")
    f3.close()

    f4 = open('log4.txt', 'w')
    f4.write("")
    f4.close()

def signin():
     while True:   
	registered = raw_input("Do you have an account? [Yes/No]")
	
	if registered.lower() == "yes":
		while True:
			id = raw_input("Username:")
			pw = raw_input("Password:")
			userlist = open('userlist.txt', 'r')
			loginuser = id+"||!^"+pw
			islogin = userlist.read()
			checklogin = islogin.split("\n")
			for index1 in range(len(checklogin)):
				if loginuser == checklogin[index1]:
					#print loginuser
					logginguser = loginuser.split("||!^")
					loguser = logginguser[0]
					print "Logged in as: %s" % (loguser)
					return loguser
			print "Username or password is invalid"
										
	elif registered.lower() == "no": 
		signup()
	
def signup():
    while True:
	newid = raw_input("Set your username:")
	newpwd = raw_input("Your password:")
	chkpwd = raw_input("Password confirmation:")
	signupdelimeter = "||!^"
	if newpwd == chkpwd:
		userlist = open('userlist.txt','r')
		existuser = newid+signupdelimeter
		content = userlist.read()

		if existuser in content:
			print "This username has already been taken"

		else:
			userlist.close()
			userlist = open('userlist.txt','a')
			insertuser = newid+signupdelimeter+newpwd
			userlist.write('%s' %(insertuser))
			userlist.write('\n')
			
			userlist.close()

			newuser = open('newuser.txt','a')
			newuser.write('%s' %(insertuser))
			newuser.write('\n')
			newuser.close()

			print "Your account has been created"
			return
	else:
		print "Password does not match"

def checktime(starttime):
	start = starttime
	end = time.time()

	elapse = end - start

	if elapse > 5:
		timetoupdate()
		start = time.time()
		#print "user sent"
	return start
	
def timetoupdate():
	newuserlist = open('userlist.txt','r')
	chkuser = newuserlist.read()
	s.sendto("***@user"+chkuser,send_address)

#Split Message
def spliter(msg, n):
	for i in xrange(0, len(msg), n):
		yield msg[i:i+n]

	
def main():
   maxtime         = 1500
   timeout         = 0
   isRoomSelected  = 0
   isSendAsk       = 0
   isFinishRequest = 0
   myAddress       = getip('wlan0')
   callThread()
   currentuser = signin()
   starttime = time.time()
   message_header = "HEADER"
   message1 = []
   message2 = []
   message3 = []
   message4 = []
   message5 = []
   full_msg1 = ""
   full_msg2 = ""
   full_msg3 = ""
   full_msg4 = ""
   full_msg5 = ""
   MTU = 1500
   isHeader1 = True
   isHeader2 = True
   isHeader3 = True
   isHeader4 = True
   isHeader5 = True
   isSendHeader1 = True
   isSendHeader2 = True
   isSendHeader3 = True
   isSendHeader4 = True
   isSendHeader5 = True


   #print starttime
   #print "This is in main loop"
   #print currentuser

   while True:
        try:
            if isRoomSelected == 0:
                if isSendAsk == 0:
                    sendRequestFiles()
                    isSendAsk =1

                while isFinishRequest == 0:
                   if timeout == maxtime:
                      isFinishRequest = 1
                   else:
                      timeout = timeout + 1

                   message, address = s.recvfrom(8192)
                   print "Merge File"

		   ##MTU:before goto merge, concat message first
		   if "***1H" in message:
		   	if message_header in message:
				message = message.split("***1H")
				data = message[1]
				message_size1 = int(str(data[len(message_header):]))
	           elif "***2H" in message:
                        if message_header in message:
                                message = message.split("***2H")
                                data = message[1]
                                message_size2 = int(str(data[len(message_header):]))
		   elif "***3H" in message:
                        if message_header in message:
                                message = message.split("***3H")
                                data = message[1]
                                message_size3 = int(str(data[len(message_header):]))
		   elif "***4H" in message:
                        if message_header in message:
                                message = message.split("***4H")
                                data = message[1]
                                message_size4 = int(str(data[len(message_header):]))
		   elif "***5H" in message:
                        if message_header in message:
                                message = message.split("***5H")
                                data = message[1]
                                message_size5 = int(str(data[len(message_header):]))
                   elif "***@1Z" in message:
                   	container = message.split("***@1Z")
                        mergefile(container[1], "log1.txt")
		   elif "***@1SZ" in message:
                   	print "Merge fragment"
                        container = message.split("***@1SZ")
                        #print container[0]+container[1]
                        message1.append(container[1])
                        full_msg1 = "".join(message1)
                        print "full_msg"+str(len(full_msg1))
                        if len(full_msg1) >= message_size1:
                        	print "msg-size"+str(message_size1)
                                mergefile(full_msg1, "log1.txt")
                        print "After Merge"
		   elif "***@2Z" in message:
                        container = message.split("***@2Z")
                        mergefile(container[1], "log2.txt")
                   elif "***@2SZ" in message:
                        print "Prepare Merge"
                        container = message.split("***@2SZ")
                        #print container[0]+container[1]
                        message2.append(container[1])
                        full_msg2 = "".join(message2)
                        print "full_msg"+str(len(full_msg2))
                        if len(full_msg2) >= message_size2:
                        	print "msg-size"+str(message_size2)
                                mergefile(full_msg2, "log2.txt")
                        print "After Merge"
		   elif "***@3Z" in message:
                        container = message.split("***@3Z")
                        mergefile(container[1], "log3.txt")
                   elif "***@3SZ" in message:
                        print "Prepare Merge"
                        container = message.split("***@3SZ")
                        #print container[0]+container[1]
                        message3.append(container[1])
                        full_msg3 = "".join(message3)
                        print "full_msg"+str(len(full_msg3))
                        if len(full_msg3) >= message_size3:
                        	print "msg-size"+str(message_size3)
                                mergefile(full_msg3, "log3.txt")
			print "After Merge"
                   elif "***@4Z" in message:
                      	container = message.split("***@4Z")
                      	mergefile(container[1], "log4.txt")
	           elif "***@4SZ" in message:
                        print "Prepare Merge"
                        container = message.split("***@4SZ")
                        #print container[0]+container[1]
                        message4.append(container[1])
                        full_msg4 = "".join(message4)
                        print "full_msg"+str(len(full_msg4))
                        if len(full_msg4) >= message_size4:
                                print "msg-size"+str(message_size4)
                                mergefile(full_msg4, "log4.txt")
                        print "After Merge"
 		   elif "***@user" in message:
		      	container = message.split("***@user")
		      	mergeuserfile(container[1], "userlist.txt")
		   elif "***@userS" in message:
                        print "Prepare Merge"
                        container = message.split("***@userS")
                        #print container[0]+container[1]
                        message5.append(container[1])
                        full_msg5 = "".join(message5)
                        print "full_msg"+str(len(full_msg5))
                        if len(full_msg5) >= message_size5:
                                print "msg-size"+str(message_size5)
                                mergefile(full_msg5, "userlist.txt")
                        print "After Merge"

                roomNumber = raw_input("Enter Room Number [1,2,3,4]: ")
                if checkBug(roomNumber):
                    isRoomSelected = 1
	            f0 = open('log'+roomNumber +'.txt', 'r') #print chat history 
    		    print(f0.read())
                    f0.close()
	    else:
                message, address = s.recvfrom(8192)
		starttime = checktime(starttime)		
                if message != "ASK-FILE":
		    if "||!^" in message:
			mergeuserfile(message,'userlist.txt')
                    elif "***@1Z" not in message and "***@2Z" not in message and "***@3Z" not in message and "***@4Z" not in message and "***@user" not in message:
	                message = message.split("|")
            
                        RCVTime  = message[0]
            	        RCVRoom  = message[1]
            	        RCVInput = message[2]
			RCVcurrentuser = message[3]
                        
                        f1 = open('log1.txt', 'a') 
                        f2 = open('log2.txt', 'a') 
                        f3 = open('log3.txt', 'a') 
                        f4 = open('log4.txt', 'a') 
	    
            	        if RCVRoom == "1" :
                    	   f1.write('%s|%s|%s|%s|%s'.rstrip('\n') %(RCVcurrentuser,address,RCVTime,RCVRoom,RCVInput))
            	        elif RCVRoom == "2" :
		    	   f2.write('%s|%s|%s|%s|%s'.rstrip('\n') %(RCVcurrentuser,address,RCVTime,RCVRoom,RCVInput))
                        elif RCVRoom == "3" :
		    	   f3.write('%s|%s|%s|%s|%s'.rstrip('\n') %(RCVcurrentuser,address,RCVTime,RCVRoom,RCVInput))
            	        elif RCVRoom == "4" :
		    	   f4.write('%s|%s|%s|%s|%s'.rstrip('\n') %(RCVcurrentuser,address,RCVTime,RCVRoom,RCVInput))

                        f1.close()
                        f2.close()
                        f3.close()
                        f4.close()
                    
            	        if RCVInput and roomNumber == RCVRoom:
                    	   print RCVcurrentuser, address , RCVTime , RCVRoom , RCVInput
	
            	else:
                    if myAddress not in address:
                        if message == "ASK-FILE":
			   print "SEND FILES"
                       	   ff1 = open('log1.txt', 'r')
                       	   ff2 = open('log2.txt', 'r')
                       	   ff3 = open('log3.txt', 'r')
                       	   ff4 = open('log4.txt', 'r')

			   readuserlist = open('userlist.txt', 'r')

                       	   file1 = ff1.read()
                       	   file2 = ff2.read()
                       	   file3 = ff3.read()
                       	   file4 = ff4.read()

		 	   alluser = readuserlist.read()
			
			   ##Handle MTU
			   if len(file1) < MTU:
  				print "file1 < MTU"
                       	   	s.sendto("***@1Z"+file1, send_address)
			   else:
				print "file1 > MTU"
				if isSendHeader1:
					header = "HEADER" + str(len(file1))
        				if (len(header) < 20):
            					blank = 20 - len(header)
            					header = header + (' ' * blank)        
					s.sendto("***1H"+header, send_address)
					isSendHeader1 = False
				for data in spliter(file1,MTU):
				        print str(len(data))
					s.sendto("***@1SZ"+data, send_address)

  			   if len(file2) < MTU:
				print "file2 < MTU"
                      	   	s.sendto("***@2Z"+file2, send_address)
			   else:
				print "file2 > MTU"
                                if isSendHeader2:
                                        header = "HEADER" + str(len(file2))
                                        if (len(header) < 20):
                                                blank = 20 - len(header)
                                                header = header + (' ' * blank)
                                        s.sendto("***2H"+header, send_address)
                                        isSendHeader2 = False
                            	for data in spliter(file2,MTU):
                                        print str(len(data))
                                        s.sendto("***@2SZ"+data, send_address)

                           if len(file3) < MTU:
				print "file3 < MTU"
                       	   	s.sendto("***@3Z"+file3, send_address)
			   else:
				print "file3 > MTU"
                                if isSendHeader3:
                                        header = "HEADER" + str(len(file3))
                                        if (len(header) < 20):
                                                blank = 20 - len(header)
                                                header = header + (' ' * blank)
                                        s.sendto("***3H"+header, send_address)
                                        isSendHeader3 = False
                                for data in spliter(file3,MTU):
                                        print str(len(data))
                                        s.sendto("***@3SZ"+data, send_address)
				
                       	   if len(file4) < MTU:
				print "file4 < MTU"
	 		   	s.sendto("***@4Z"+file4, send_address)
			   else:
				print "file4 > MTU"
                                if isSendHeader4:
                                        header = "HEADER" + str(len(file4))
                                        if (len(header) < 20):
                                                blank = 20 - len(header)
                                                header = header + (' ' * blank)
                                        s.sendto("***4H"+header, send_address)
                                        isSendHeader4 = False
                                for data in spliter(file4,MTU):
                                        print str(len(data))
                                        s.sendto("***@4SZ"+data, send_address)

			   if len(alluser) < MTU:
				print "alluserfile < MTU"
			   	s.sendto("***@user"+alluser, send_address)
			   else:
				print "alluserfile > MTU"
                                if isSendHeader5:
                                        header = "HEADER" + str(len(alluser))
                                        if (len(header) < 20):
                                                blank = 20 - len(header)
                                                header = header + (' ' * blank)
                                        s.sendto("***5H"+header, send_address)
                                        isSendHeader5 = False
                                for data in spliter(alluser,MTU):
                                        print str(len(data))
                                        s.sendto("***@userS"+data, send_address)


                           ff1.close()
                           ff2.close()
                           ff3.close()
                           ff4.close()
			   readuserlist.close()

			   print "END SEND FILES"			
	except:
            pass

        input = getLine()
        if input:
            localtime = time.asctime(time.localtime(time.time()))
            s.sendto(localtime+"|"+roomNumber+"|"+input+"|"+currentuser, send_address)

if __name__ == '__main__':
    main()
