from TelemeterService import TelemeterService, TelemeterUsageData

username = "username"
password = "password"

def handleResponse(response):
    print "monthly usage\n-------------"
    print "volume limit: " + str(response.limit) + " " + response.unit
    print "volume used:  " + str(response.totalUsage) + " " + response.unit
    print "volume left:  " + str(response.limit - response.totalUsage) + " " + response.unit
    print "last calculation: " + str(response.timestamp)
    print "validity period: " + str(response.dailyUsage[0].day) + " until " + str(response.dailyUsage[-1].day)

    print "\ndaily usage\n-----------"

    for day in response.dailyUsage:
        print str(day.day) + " : " + str(day.usage) + " " + response.unit



# script entrypoint
try:
    service = TelemeterService(username, password)
    print "contacting telemeter service...\n"
    response = service.fetchData()
    handleResponse(response)
except Exception as ex:
    print "an error occured: ", ex



