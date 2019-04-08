# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license
"""
    This script scans for the Node Controller IP address and writes it to a file.

"""
#TODO can be added to a process in communicator to periodically scan for NC and send registration if needed
import subprocess, os, socket, re

#need to find the node's IP address 
#so, first save results of ifconfig and grep commands to get IP address to a file
p = subprocess.Popen('ifconfig | grep "inet addr" > output.txt', stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()

#read the file
with open('output.txt','r') as _file:
    line = _file.readline().strip()

#the device's IP address should be found in the first line
#The line should look like '     inet address:xx.xx.xx.xx  Bcast:xx.xx.xx.xx Mask:xx.xx.xx.xx   '
#remove 'inet address'
junk, IP_addr = line.split(':',1)

#remove the extra stuff on the end that we don't need
IP_addr, junk = IP_addr.split(' ', 1)

#Now, we have the device's IP address. We can use that to scan for the node controller
#Need to remove the last number and add '.1/24'
nmap_IP = ''
for i in range(3):
    stuff, IP_addr = IP_addr.split('.',1)
    nmap_IP = nmap_IP + stuff + '.'

#this is used to run an nmap scan to discover hosts
nmap_IP = nmap_IP + '1/24'

#need to do a host discovery scan and write results to file
p = subprocess.Popen('nmap -sP ' + nmap_IP, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
_file = open('output.txt', 'w')
_file.writelines(output)
_file.close()

#list of available hosts that need to be checked

with open ('output.txt','r') as _file:
    lines = _file.read()
 
hosts = re.findall( r'[0-9]+(?:\.[0-9]+){3}', lines)

#TODO for robustness, go through all 255 addresses in subnet
#now, we need to check each host to find out if it is the node controller
PORT = 9090 #port for push_server
for HOST in hosts:
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        print 'Connected...'
        request = 'Hello' #a nice hello
        s.send(request)
        msg = s.recv(4028)
        if msg == 'Hi': #Nodecontroller! #TODO arbitrary 
            with open('/etc/waggle/NCIP','w') as file_: #write nodecontroller IP to file
                file_.write(HOST)
            msg = s.recv(4028)#waits for node controller to send ID 
            #Node controller unique ID is neccessary for registration
            with open('/etc/waggle/NCID','w') as file_: #write nodecontroller ID to file
                file_.write(msg)
            #TODO send registration here
            s.close()
            break
        else:
            #Not the nodecontroller... 
            s.close()
    except: 
        #Not the nodecontroller....
        pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

