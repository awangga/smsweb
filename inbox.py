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

form = cgi.FieldStorage()

#rcpt = form["rcpt"].value
#msg = form["msg"].value

sw = smsweb.SmsWeb()
sw.openser()
sw.opendb()
lmsg=sw.listInbox()
for msgidx in lmsg:
	pdu=getPDU(msgidx)
	data =decodePDU(pdu)
	sw.insertInbox(data)
	sw.deleteMsg(msgidx)
sw.close