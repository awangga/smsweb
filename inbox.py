#!/usr/bin/env python
"""
inbox.py -  Program to :
1. read message inbox list index, 
2. read it and save to db and delete message
"""
print "Content-Type: text-html"
print
import cgitb
cgitb.enable()
import cgi
import smsweb
import subprocess
import json 
from bson import json_util

form = cgi.FieldStorage()

#rcpt = form["rcpt"].value
#msg = form["msg"].value

sw = smsweb.SmsWeb()
#sw.openser()
sw.opendb()


if not id: 
	print sw.getInbox(id)
else:
	for a in sw.getInboxs():
		print json.dumps(a, default=json_util.default)
		#print a