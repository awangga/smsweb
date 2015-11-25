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
sw.openser()
sw.moveInboxtodb()
dt=sw.getInbox()
while dt:
	text = dt["text"].split('#')
	if (len(text) > 1) and (len(text[0]) < 20):
		sw.insertCommands(dt["number"],dt["text"],dt["date"])
	else:
		sw.insertComments(dt["number"],dt["text"],dt["date"])
	sw.removeInbox(dt["_id"])
	dt=sw.getInbox()
print "Done..."
