#!/usr/bin/env python
"""
config.py 
please make sure your webserver user was added to group dialout
make sure serial set permission to 660 with group dialout
"""

def success():
    print "Success to send!"
#set to mainapi.py for sending by web API sms, or main.py for sending using modem
mode="main.py"

serial = "/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0"
recipient = '+6281312000300'
message = "Neng...!!! ieu mamah pake HP batur.. mamah keur aya masalah di kantor polisi.. mamah menta tulung pang nganteurkeun cai sa ember... inget cai sa ember ... lain pulsa...pulsa mah loba keneh...mamah keur milu ngising di kantor polisi... caina saat ... burukeun ulah seuri... mamah can cebok yeuh, inget nya neng.. cai sa ember ..!!! lain pulsa...!!! mamah geus cangkeul nagog"
port = 8181
timeout = 30

#posting data to http, for this exapmple http://urltoapi/&msisdn=0813120003000&message=bawangmerah
urlapi = "http://urltoapi/"
rcptparamapi = "&msisdn="
msgparamapi = "&message="

mongohost = "localhost"
mongoport = 27017
