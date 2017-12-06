#!/usr/bin/env python
#Author: jianwei.hu@windriver.com
#Date: 2017/12/6

import sys
import commands
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import socket
import os,time

path = os.path.abspath(os.curdir)
build = os.path.split(os.path.split(os.path.abspath(os.curdir))[0])[1]
hostname = socket.gethostname()
build_time = time.ctime(time.time())

sender = 'wr-taf@windriver.com'
receivers = ['jianwei.hu@windriver.com']

if sys.argv[1] == "FAILED":
     output1 = "FAILED"
else:
     more_file = 'cat '+sys.argv[1]
     (status1, output1) = commands.getstatusoutput(more_file)
more_file3 = 'cat ../build.cmd'
(status1, output3) = commands.getstatusoutput(more_file3)
more_file2 = 'git log'
(status1, output2) = commands.getstatusoutput(more_file2)

content='['+build_time+']'+"Build server and path:   \n"+hostname+":"+path+" \n"+"Logs:--->\n"+ output3 +"\n"+output2 +"\n" + output1
message = MIMEText(content, 'plain', 'utf-8')
message['From'] = Header("Hu Jianwei", 'utf-8')
message['To'] =  Header("Hu Jianwei", 'utf-8')

subject = '['+hostname +'] '+build+' '+sys.argv[2]+' build finished!!!'
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP('147.11.189.50','25')
    smtpObj.sendmail(sender, receivers, message.as_string())
    print "send build email Successfully"
except smtplib.SMTPException:
    print "Error: unable to send email"
