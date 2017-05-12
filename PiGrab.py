import os
import sys
import subprocess
#from tkinter import *
import time

#time.sleep(60)

def ping():
    #ip of file server
    ip = "192.168.255.46"
    response = os.system("ping -c 4 " + ip)
    if response == 0:
        print(ip , 'is reachable')
    else:
        print(ip , 'is unreachable.')

def getserial():
    #need to add check to make sure the serial actually was grabbed
    cpuinfo=subprocess.Popen("cat /proc/cpuinfo | grep Serial | cut -d' ' -f2", stdout=subprocess.PIPE, shell=True)
    output_bytes, err = cpuinfo.communicate()
    output_string = str(output_bytes, 'utf-8')
    output_string = output_string.strip('\n')
    print(output_string)
    return output_string
    
def getmacaddr():
    #need to add check to make sure the macaddr actually was grabbed
    ifconfig=subprocess.Popen("ifconfig eth0 | grep HWaddr |cut -dH -f2|cut -d\  -f2", stdout=subprocess.PIPE, shell=True)
    if_output_bytes, err = ifconfig.communicate()
    if_output_string = str(if_output_bytes, 'utf-8')
    if_output_string = if_output_string.rstrip('\n')
    print(if_output_string)
    return if_output_string

def is_mount():
    #what the mount point should look like
    mount_should="//192.168.255.46/AmazonPi"
    mount_point=subprocess.Popen("df | grep AmazonPi | cut -d\  -f1", stdout=subprocess.PIPE, shell=True)
    mount_output_bytes, err = mount_point.communicate()
    mount_output_string = str(mount_output_bytes, 'utf-8')
    #removes line break after mount point
    mount_output_string = mount_output_string.rstrip('\n')
    if mount_output_string == mount_should:
        print(mount_output_string + " is mounted")
    else:
        print(mount_output_string + " not mounted")
            
    return mount_output_string

def asset_tag():
    try:
        tag_number1 = int(input("Please type asset tag number: "))
    except:
        input("Something is wrong with your input. Press Enter to restart the script. :")
        return asset_tag()
    #empty check is handlded by the integer input. Empty space is not an integer
    #need to print something to console if a non integer is entered
    tag_number2 = int(input("Please retype Asset tag number: "))
    if str(tag_number1) == str(tag_number2):
        tag_number=tag_number1
        print("Asset tag number is %d" % tag_number)           
        return tag_number
    else:
        input("Asset tag numbers did not match. Press Enter to restart the script. :")
        return asset_tag()
        


def create_text_file(tag_number, serial, macaddr):
    file=open("/home/pi/Desktop/SharedFolder/%d.txt" % tag_number, "w")
    file.write("Asset Tag number: %d  " % tag_number)
    file.write("Serial: %s  " % serial)
    file.write("MAC Address: %s " % macaddr)
    file.close()
    
    

def main():
    ping()
    is_mount()
    tag_number=asset_tag()
    serial=getserial()
    macaddr=getmacaddr()
    create_text_file(tag_number, serial, macaddr)



main()
    




