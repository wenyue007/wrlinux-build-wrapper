#!/usr/bin/env python
# jianwei.hu@windriver.com

import sys
import commands
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart 
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.header import Header
import email.encoders as encoders
import socket
import os,time

path = os.path.abspath(os.curdir)
build = os.path.split(os.path.split(os.path.abspath(os.curdir))[0])[1]
hostname = socket.gethostname()
build_time = time.ctime(time.time())
file = (r"../build.cmd")

msg = MIMEMultipart() 
msg['From'] = Header("Hu Jianwei", 'utf-8')
msg['To'] =  Header("Hu Jianwei", 'utf-8')

sender = 'jianwei.hu@windriver.com'
receivers = ['jianwei.hu@windriver.com']

if sys.argv[1] == "FAILED":
     output1 = "FAILED"
     more_file = output1
elif sys.argv[1] == "rebuild":
     output1 = "Rebuild passed!"
     more_file = output1
else:
     more_file = 'cat '+sys.argv[1]
     (status1, output1) = commands.getstatusoutput(more_file)

more_file3 = "sed '/^\/folk\/jhu2/,/^\s*Filter error\/warning/!d' ../build.cmd"
more_file3 = more_file3 + "\n" + "cat ../build.cmd | grep -iE ':warning:|:error:'|sort|uniq"
(status1, output3) = commands.getstatusoutput(more_file3)
more_file2 = 'git log'
(status1, output2) = commands.getstatusoutput(more_file2)

if sys.argv[2] == "re":
    test_type = "re"
else:
    test_type = sys.argv[2] + " "

subject = '['+hostname +'] '+build+' '+test_type+'build finished!!!'
msg['Subject'] = Header(subject, 'utf-8')

content='['+build_time+']'+ "\n"+"Build server and path:   \n"+hostname+":"+path+" \n"+"\n"+\
         "Logs:--->(cat build.cmd)\n" + output3 +"\n\n" + \
         "git log \n" + output2 + "\n\n" + \
         output1

body = MIMEText(content, 'plain', 'utf-8')
msg.attach(body) 

att1 = MIMEText(open('../build.cmd','r').read()) 
att1.add_header('Content-Disposition', 'attachment', filename="build.txt")
msg.attach(att1) 

try:
    smtpObj = smtplib.SMTP('147.11.189.50','25')
    smtpObj.sendmail(sender, receivers, msg.as_string())
    print "send build email Successfully"
except smtplib.SMTPException:
    print "Error: unable to send email"

smtpObj.close()
