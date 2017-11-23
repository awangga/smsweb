#!/usr/bin/env python
"""
main.py - Main Program to :
1. get from outbox, 
2. sent sms via modem
3. insert to sentitems
"""
import smsweb

sw = smsweb.SmsWeb()
sw.opendb()
dt=sw.getOutbox()
sw.openser()
while dt:
	sw.rcpt(dt["rcpt"])
	sw.msg(dt["msg"])
	sw.idProcess(dt["_id"])
	sw.sends()
	sw.removeOutbox(dt["_id"])
	dt=sw.getOutbox()

print "Done...sending"

sw.moveInboxtodb()
dt=sw.getInbox()
while dt:
	sw.rcpt(dt["number"])
	sw.msg(dt["text"])
	sw.idProcess(dt["_id"])
	sw.apisends()
	text = dt["text"].split('#')
	if (len(text) > 1) and (len(text[0]) < 20):
		sw.insertCommands(dt["number"],dt["text"],dt["date"])
	else:
		sw.insertComments(dt["number"],dt["text"],dt["date"])
	sw.removeInbox(dt["_id"])
	dt=sw.getInbox()
print "Done...parsing"