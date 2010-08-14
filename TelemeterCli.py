from TelemeterService import TelemeterService, TelemeterUsageData
import sys


service = TelemeterService("username", "password")
print "contacting telemeter service...\n"
response = service.fetchData()
print "monthly usage\n-------------"
print "volume limit: " + str(response.limit) + " " + response.unit
print "volume used:  " + str(response.totalUsage) + " " + response.unit
print "volume left:  " + str(response.limit - response.totalUsage) + " " + response.unit
print "last calculation: " + str(response.timestamp)
print "validity period: " + str(response.dailyUsage[0].day) + " until " + str(response.dailyUsage[-1].day)

print "\ndaily usage\n-----------"

for day in response.dailyUsage:
    print str(day.day) + " : " + str(day.usage) + " " + response.unit


