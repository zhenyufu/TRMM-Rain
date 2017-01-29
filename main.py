from rain import *

print "MAIN: This is the main script"
dataSpanish = readSpanish("raw_senamhi/");
for data in dataSpanish:
    print data.fileName
    print data.startDate
    print data.endDate




#print len(dataSpanish[0])
#print len(dataSpanish[0][0])

