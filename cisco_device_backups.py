#!/usr/local/bin/python3

####################################################
#     Device Backup Script for Cisco Devices       #
####################################################
# Required Modules #
import ftplib
import datetime
import sys
import paramiko
from time import sleep
from csv import reader

########################################
# Credentials and save_path initiation #
########################################
# Device credentials (common on all devices) 
# Sample info, change accordingly
uname = 'uname'
pswd = 'pw'

# TFTP access details
tftp_server_ip = '10.10.10.200'



###################################################################
# open SSH session and write configs to tftp server               #
###################################################################
def device_tftp(ip, uname, pswd, filename):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, port=22, username=uname, password=pswd)
        print ('***Connected to ' + ip + '\t*******')
        channel = ssh.invoke_shell()
        channel.send('en\n')
        sleep(4)
        channel.send(pswd + '\n')
        sleep(4)
        send_string = 'copy run start\n'
        channel.send('copy run start\n\n')
        sleep(2)
        send_string = 'show run | redirect tftp://' + tftp_server_ip  + '/' + filename + '\n'
        channel.send('show run | redirect tftp://' + tftp_server_ip  + '/' + filename + '\n')
        sleep(10)
        ssh.close()
    except:
        print ('cannot connect to ' + ip)
    return

###################################################################
# read IP and hostname into dictionary #
###################################################################
def read_ip_host(csv_file):
  with open(csv_file, 'r') as read_obj:
      csv_reader = reader(read_obj)
      device_list = list(csv_reader)
      return (device_list)


devices = read_ip_host('device_list.csv')
for item in devices:
    fname = 'config.' + item[0]
    device_tftp(item[1], uname, pswd, fname)



