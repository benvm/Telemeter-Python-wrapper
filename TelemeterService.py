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

from datetime import date, datetime, time
from xml.dom import minidom
import dateutil.parser
import urllib
import urllib2
import base64

# contains traffic data for one day
class TelemeterDailyUsageData:
    day = date.today()
    usage = 0


# contains the full response data
class TelemeterUsageData:
    timestamp = datetime.now()
    timestampExpired = datetime.now()
    unit = "MB"
    limit = 0
    totalUsage = 0
    dailyUsage = []


# actual service encapsulation class
class TelemeterService:
    username = ""
    password = ""
    usageData = TelemeterUsageData()


    def __init__(self, username, password):
        self.username = username
        self.password = password

    def fetchData(self):
        url = 'https://t4t.services.telenet.be/TelemeterService'
        data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:tel=\"http://www.telenet.be/TelemeterService/\"><soapenv:Header/><soapenv:Body><tel:RetrieveUsageRequest><UserId>" + self.username + "</UserId><Password>" + self.password + "</Password></tel:RetrieveUsageRequest></soapenv:Body></soapenv:Envelope>"
        headers = {
            'Content-Type': 'text/xml',
            'Content-Length': len(data),
        }
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req, data).read()
        return self.parseResponse(response)

    def parseResponse(self, responsedata):
        # parse the xml
        xmldoc = minidom.parseString(responsedata)
        self.usageData = TelemeterUsageData()

        # get simple fields
        self.usageData.limit = int(xmldoc.getElementsByTagName("Limit")[0].childNodes[0].data)
        self.usageData.totalUsage = int(xmldoc.getElementsByTagName("TotalUsage")[0].childNodes[0].data)
        self.usageData.unit = xmldoc.getElementsByTagName("Unit")[0].childNodes[0].data
        self.timestamp = dateutil.parser.parse(xmldoc.getElementsByTagName("Timestamp")[0].childNodes[0].data)

        return self.usageData
