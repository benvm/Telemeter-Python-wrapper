from TelemeterService import TelemeterService, TelemeterVolumeData, TelemeterFUPData
import sys
import getpass


def handleResponse(response):
    
    if isinstance(response, TelemeterVolumeData):
        print "monthly usage\n-------------"
        print "volume limit: " + str(response.limit) + " " + response.unit
        print "volume used:  " + str(response.totalUsage) + " " + response.unit
        print "volume left:  " + str(response.limit - response.totalUsage) + " " + response.unit
        print "last calculation: " + str(response.timestamp)
        print "validity period: " + str(response.dailyUsage[0].day) + " until " + str(response.dailyUsage[-1].day)

        print "\ndaily usage\n-----------"

        for day in response.dailyUsage:
            print str(day.day) + " : " + str(day.usage) + " " + response.unit
    
    elif isinstance(response, TelemeterFUPData):
        print "FUP\n---"
        print "used: " + str(response.totalUsage) + " " + response.unit
        print "minimum: " + str(response.minUsage) + " " + response.unit
        print "maximum: " + str(response.maxUsage) + " " + response.unit
        print "last update: " + str(response.lastUpdate)
        print "status: " + response.status

    else:
        print "Error: No valid response retrieved"

# script entrypoint

if len(sys.argv) < 2:
    print "usage: TelemeterCli.py username [password]"
    sys.exit()

username = sys.argv[1]

if len(sys.argv) == 3:
    password = sys.argv[2]
else:
    password = getpass.getpass()

try:
    service = TelemeterService(username, password)
    response = service.fetchData()
    handleResponse(response)
except Exception as ex:
    print "an error occured: ", ex


