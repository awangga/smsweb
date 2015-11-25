#!/usr/bin/env python
"""
insert.py -  Program to :
1. insert to outbox collection, 
2. check if main is running? if not run then run
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

#form = cgi.FieldStorage()

#rcpt = form["rcpt"].value
#msg = form["msg"].value

sw = smsweb.SmsWeb()
#sw.openser()
sw.opendb()
for a in sw.getComments():
	print json.dumps(a, default=json_util.default)
	#sw.removeComments(a["_id"])
	#print a