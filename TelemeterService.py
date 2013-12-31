# Copyright (C) 2010 Steven Van Bael <steven.v.bael@gmail.com>
#
# This file is part of Telemeter Python wrapper.
#
# Telemeter Python wrapper is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Telemeter Python wrapper is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Telemeter Python wrapper.  If not, see <http://www.gnu.org/licenses/>.
#
# Support for FUP type subscription: Copyright (C) 2013 Ben Van Mechelen benvm.be@gmail.com

from datetime import date, datetime, time
from xml.dom import minidom
from datetime import datetime
from urllib.request import urlopen, Request
import base64

# contains traffic data for one day
class TelemeterDailyUsageData:
    day = date.today()
    usage = 0


# contains the full response data
class TelemeterVolumeData:
    timestamp = None
    timestampExpired = None
    unit = None
    limit = 0
    totalUsage = 0
    dailyUsage = []
    
class TelemeterFUPData:
    timestamp = None
    expiryTimestamp = None
    lastUpdate = None
    unit = None
    minUsage = 0
    MaxUsage = 0
    totalUsage = 0
    periodFrom = None
    periodTill = None
    periodDay = 0
    status = None
    statusNL = None
    statusFR = None
    startGrootverbruiker = None
    startVrijVerbruik = None
        

# actual service encapsulation class
class TelemeterService:
    username = ""
    password = ""

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def fetchData(self):
        url = 'https://t4t.services.telenet.be/TelemeterService'
        data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:tel=\"http://www.telenet.be/TelemeterService/\"><soapenv:Header/><soapenv:Body><tel:RetrieveUsageRequest><UserId>" + self.username + "</UserId><Password>" + self.password + "</Password></tel:RetrieveUsageRequest></soapenv:Body></soapenv:Envelope>"
        data = data.encode('utf8')
        headers = {
            'Content-Type': 'text/xml',
            'Content-Length': len(data),
        }
        req = Request(url, data, headers)
        response = urlopen(req, data).read()
        return self.parseResponse(response)
        

    def parseResponse(self, responsedata):
        # parse the xml
        xmldoc = minidom.parseString(responsedata)
        
        # See if we received a fault
        fault = xmldoc.getElementsByTagName("TelemeterFault")
        if fault:
            code = fault.getElementsByTagName("Code")[0].childNodes[0].data
            description = fault.getElementsByTagName("Description")[0].childNodes[0].data
            raise RuntimeError(code + ": " + description)
        
        ticket = xmldoc.getElementsByTagName("Ticket")
        fup = xmldoc.getElementsByTagName("FUP")
        volume = xmldoc.getElementsByTagName("Volume")
        
        
        if fup:
            # FUP subsription
            fup = fup[0]
            self.usageData = TelemeterFUPData()
            
            for key in {"Period", "Usage", "Status", "StatusDescription", "Info"}:
                nl = fup.getElementsByTagName(key)
                if key is "Period":
                    #ignoring UTC offset for now.
                    self.usageData.periodFrom = datetime.strptime(nl[0].getElementsByTagName("From")[0].childNodes[0].data[:-6], '%Y-%m-%d')
                    self.usageData.periodTill = datetime.strptime(nl[0].getElementsByTagName("Till")[0].childNodes[0].data[:-6], '%Y-%m-%d')
                    self.usageData.periodDay = int(nl[0].getElementsByTagName("CurrentDay")[0].childNodes[0].data)
                if key is "Usage":
                    self.usageData.totalUsage = float(nl[0].getElementsByTagName("TotalUsage")[0].childNodes[0].data)
                    self.usageData.unit = nl[0].getElementsByTagName("Unit")[0].childNodes[0].data
                    self.usageData.minUsage = float(nl[0].getElementsByTagName("MinUsageRemaining")[0].childNodes[0].data)
                    self.usageData.maxUsage = float(nl[0].getElementsByTagName("MaxUsageRemaining")[0].childNodes[0].data)
                    self.usageData.lastUpdate = datetime.strptime(nl[0].getElementsByTagName("LastUpdate")[0].childNodes[0].data[:-10], '%Y-%m-%dT%H:%M:%S')
                if key is "Status":
                    self.usageData.status = nl[0].childNodes[0].data
                if key is "StatusDescription":
                    self.usageData.statusNL = nl[0].getElementsByTagName("NL")[0].childNodes[0].data
                    self.usageData.statusFR = nl[0].getElementsByTagName("FR")[0].childNodes[0].data
                if key is "Info":
                    if nl:
                        self.usageData.startGrootverbruiker = datetime.strptime(nl[0].getElementsByTagName("StartGrootverbruiker")[0].childNodes[0].data[:-6], '%Y-%m-%d')
                        self.usageData.startVrijVerbruik = datetime.strptime(nl[0].getElementsByTagName("StartVrijVerbruik")[0].childNodes[0].data[:-6], '%Y-%m-%d')
            

        elif volume:
            # Volume subscription
            volume = volume[0]
            self.usageData = TelemeterVolumeData()

            # get simple fields
            self.usageData.limit = int(volume.getElementsByTagName("Limit")[0].childNodes[0].data)
            self.usageData.totalUsage = int(volume.getElementsByTagName("TotalUsage")[0].childNodes[0].data)
            self.usageData.unit = volume.getElementsByTagName("Unit")[0].childNodes[0].data
            

            # get daily usage data for 30 days
            days = vol.getElementsByTagName("DailyUsage")
            for xmlDay in days:    
                usage = TelemeterDailyUsageData()
                daystr = xmlDay.childNodes[0].childNodes[0].data
                usage.day = date(int(daystr[0:4]),int(daystr[5:7]),int(daystr[8:10]))
                usage.usage = xmlDay.childNodes[1].childNodes[0].data
                self.usageData.dailyUsage.append(usage)


        if ticket:
            # Ticket
            ticket = ticket[0]
            self.usageData.timestamp = datetime.strptime(ticket.getElementsByTagName("Timestamp")[0].childNodes[0].data[:-10], '%Y-%m-%dT%H:%M:%S')
            self.usageData.expiryTimestamp = datetime.strptime(ticket.getElementsByTagName("ExpiryTimestamp")[0].childNodes[0].data[:-10], '%Y-%m-%dT%H:%M:%S')
            
            
        return self.usageData
        
        
        
