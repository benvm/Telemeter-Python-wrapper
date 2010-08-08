from TelemeterService import TelemeterService, TelemeterUsageData

print "starting execution"
service = TelemeterService("username", "password")
print "fetching data"
response = service.fetchData()
print "fetch complete"
print "limit: " + str(response.limit)
print "total: " + str(response.totalUsage)
