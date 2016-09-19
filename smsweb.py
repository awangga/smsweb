#!/usr/bin/env python
"""
smsweb : spy mongoDB connector
"""
import config
import os.path
import re
import time
import pymongo
import urllib2
from datetime import datetime
import serial
from messaging.sms import SmsSubmit
from messaging.sms import SmsDeliver

class SmsWeb(object):
    def __init__(self, recipient=config.recipient, message=config.message):
        self.recipient = recipient
        self.content = message

    def openser(self):
        self.ser = serial.Serial(config.serial, 115200, timeout=config.timeout)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.SendCommand('ATZ\r',8)
        self.SendCommand('AT+CMGF=0\r',16)

    def opendb(self):
	    self.conn = pymongo.MongoClient(config.mongohost, config.mongoport)
	    self.db = self.conn.smsweb
    
    def insertOutbox(self,rcpt,msg):
	    self.db.outbox
	    doc = {"rcpt":rcpt,"msg":msg,"timestamp":datetime.now()}
	    idProcess = self.db.outbox.insert_one(doc).inserted_id
	    ret = {"rcpt":rcpt,"msg":msg,"idProcess":idProcess}
	    return ret
	
    def insertOutboxPerRcpt(self,rcpt,msg):
	    self.db.outbox
	    rcptarr = re.split(',|;',rcpt)
	    ret = 0
	    for num in rcptarr:
			if num:
				doc = {"rcpt":num,"msg":msg,"timestamp":datetime.now()}
				idProcess = self.db.outbox.insert_one(doc).inserted_id
				ret = ret + 1
	    kemb = {"Total Nomor Tujuan":ret,"Pesannya":msg}
	    return kemb
    
    def insertSentitem(self,rcpt,msg,stat):
	    self.db.sentitems
	    doc = {"rcpt":rcpt,"msg":msg,"timestamp":str(datetime.now()),"idProcess":self.idprocess,"stat":stat}
	    return self.db.sentitems.insert_one(doc).inserted_id
    
    def insertErrornum(self):
	    self.db.errornum
	    doc = {"rcpt":self.recipient,"msg":self.content,"timestamp":datetime.now()}
	    idProcess = self.db.errornum.insert_one(doc).inserted_id
	    return doc
    
    def insertInbox(self,data):
	    self.db.inbox
	    return self.db.inbox.insert_one(data).inserted_id
	    
    def insertCommands(self,rcpt,msg,rcvdate):
	    self.db.commands
	    data = {"from":rcpt,"msg":msg,"timestamp":rcvdate}
	    return self.db.commands.insert_one(data).inserted_id
	    
    def insertComments(self,rcpt,msg,rcvdate):
	    self.db.comments
	    data = {"from":rcpt,"msg":msg,"timestamp":rcvdate}
	    return self.db.comments.insert_one(data).inserted_id
	    
    def getErrors(self):
	    self.db.errornum
	    return self.db.errornum.find()
    
    def getSentitem(self,id):
	    self.db.sentitems
	    return self.db.sentitems.find_one({"idProcess":id})
	    
    def getSentitems(self):
	    self.db.sentitems
	    return self.db.sentitems.find()
	    
    def getOutbox(self):
	    self.db.outbox
	    return self.db.outbox.find_one()
	
    def getOutboxs(self):
	    self.db.outbox
	    return self.db.outbox.find()
    
    def getInbox(self):
	    self.db.inbox
	    return self.db.inbox.find_one()
    
    def getInboxs(self):
	    self.db.inbox
	    return self.db.inbox.find()
	    
    def getCommands(self):
	    self.db.commands
	    return self.db.commands.find()
	    
    def getComments(self):
	    self.db.comments
	    return self.db.comments.find()
	    
    def removeOutbox(self,id):
	    self.db.outbox
	    return self.db.outbox.delete_many({"_id":id})
	    
    def removeInbox(self,id):
	    self.db.inbox
	    return self.db.inbox.delete_many({"_id":id})
	    
    def removeCommands(self,id):
	    self.db.commands
	    return self.db.commands.delete_many({"_id":id})
	    
    def removeComments(self,id):
	    self.db.comments
	    return self.db.comments.delete_many({"_id":id})
	    
    def dropOutbox(self):
    	self.db.outbox
    	self.db.drop_collection("outbox")
    
    def rcpt(self, number):
        self.recipient = number

    def msg(self, message):
        self.content = message

    def idProcess(self,idprocess):
	    self.idprocess = idprocess

    def apisends(self):
            rcptarr = re.split(',|;',self.recipient)
            for num in rcptarr:
                if num:
                        print '*Sending SMS to: '+num+' \n'
                        number = self.validateNumber(num)
                        self.rcpt(number)
                        try:
                                self.apisend()
                        except ValueError:
                                self.insertErrornum()
   
    def apisend(self):
	msg = urllib2.quote(self.content)
	apistr = config.urlapi+config.rcptparamapi+self.recipient+config.msgparamapi+msg
	data = urllib2.urlopen(apistr).read()
        return data
    
    def sends(self):
	    rcptarr = re.split(',|;',self.recipient)
	    for num in rcptarr:
	    	if num:
		    	print '*Sending SMS to: '+num+' \n'
		    	number = self.validateNumber(num)
		    	self.rcpt(number)
		    	try:
		    		self.send()
		    	except ValueError:
		    		self.insertErrornum()
    
    def send(self):
        self.pdu = SmsSubmit(self.recipient, self.content)
        for xpdu in self.pdu.to_pdu():
	        command = 'AT+CMGS=%d\r' % xpdu.length
	        a = self.SendCommand(command,len(str(xpdu.length))+14)
	        command = '%s\x1a' % xpdu.pdu
	        b = self.SendCommand(command,len(xpdu.pdu)+20)
	        data = str(a)+str(b)
	        self.insertSentitem(self.recipient,self.content,data)
        return data
	         
    def validateNumber(self,num):
	    num = num.replace(" ", "")
	    return num
    
    def close(self):
        self.ser.close()

    def SendCommand(self,command,char,getline=True):
        self.ser.write(command)
        data = ''
        if getline:
            data=self.ReadLine(char)
        return data 
        
    def ReadAll(self):
    	data = self.ser.readall()
    	return data
    
    def ReadLine(self,char):
        data = self.ser.read(char)
        return data

    def unreadMsg(self):
        self.ser.flushInput()
        self.ser.flushOutput()
        command = 'AT+CMGL=0\r\n'
        data = self.SendCommand(command,16)
        return data
        
    def fetchInbox(self):
        self.ser.flushInput()
        self.ser.flushOutput()
        command = 'AT+CMGL=4\r\n'
        self.ser.write(command)
        cmd = self.ser.readline()#'AT+CMGL=4\r\n'
        cmd += self.ser.readline()#'\r\n'
        a = []
        cmglstat = self.ser.readline()#'+CMGL: 1,0,,24\r\n'
        while "+CMGL:" in cmglstat:
        	idx = cmglstat.rstrip().split(',')[0].split(' ')[1]
        	data = self.ser.readline()#'0791269846100129040D91269816707009F10000511152511252820433972C06\r\n'
        	a.append(int(idx))
        	cmglstat = self.ser.readline()#if ada lagi '+CMGL: 10,2,,32\r\n' if abis '\r\n'
        #ok = self.ser.readline()#if abis 'OK\r\n'
        return a
        
    def listInbox(self):
        self.ser.flushInput()
        self.ser.flushOutput()
        command = 'AT+CMGL=1\r\n'
        self.ser.write(command)
        cmd = self.ser.readline()
        cmd += self.ser.readline()
        head = self.ser.readline()
        a = []
        while "CMGL" in head:
	        data = self.ser.readline()
	        sms = SmsDeliver(data.rstrip())
	        idx = head.rstrip().split(',')[0].split(' ')[1]
	        self.insertInbox(sms.data)
	        #print idx
	        a.append(int(idx))
	        head = self.ser.readline()
        return a

    def allMsg(self):
        self.ser.flushInput()
        self.ser.flushOutput()
        command = 'AT+CMGL=4\r\n'
        data = self.SendCommand(command,16)
        return data
        
    def deleteMsg(self, idx):
        self.ser.flushInput()
        self.ser.flushOutput()
        command = 'AT+CMGD=%s\r\n' % idx
        self.ser.write(command)
        data = self.ser.readline()
        data += self.ser.readline()
        data += self.ser.readline()
        return data

    def decodePDU(self, data):
	    sms = SmsDeliver(data)
	    return sms.data
    
    def deleteMsgs(self, idx):
        #self.ser.flushInput()
        #self.ser.flushOutput()
        for id in idx:
	        command = 'AT+CMGD=%s\r\n' % id
	        self.SendCommand(command,18)
        
    def getPDU(self, idx):
        self.ser.flushInput()
        self.ser.flushOutput()
        command = 'AT+CMGR=%s\r\n' % idx
        self.ser.write(command)
        data = self.ser.readline()
        while not "+CMGR: " in data:
        	data = self.ser.readline()
        data = self.ser.readline()
        pdu = data.rstrip()
        return pdu        
    
    def moveInboxtodb(self):
	    lmsg=self.fetchInbox()
	    print lmsg
	    if lmsg:
	    	for msgidx in lmsg:
	    		pdu=self.getPDU(msgidx)
	    		data =self.decodePDU(pdu)
	    		print pdu
	    		self.insertInbox(data)
	    		print "insert success"
	    		self.deleteMsg(msgidx)
	    		print "msg deleted"
	    return lmsg
    
    def isRunning(self,pid):
    	path = "/proc/"+str(pid)
    	return os.path.exists(path)
    	#try:
    	#	os.kill(pid,0)
    	#except OSError:
    	#	return False
    	#else:
    	#	return True
    	
