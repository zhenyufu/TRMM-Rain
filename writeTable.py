from rain import *

f = open('_data/dataSpanish_0.8.3', 'rb')
dataSpanish = pickle.load(f)

myFile = hostPath + "table.csv"
myHandler = open(myFile,"w")
myWriter = csv.writer(myHandler)
row = ["fileName", "mapId", "Lat", "Lon", "Elevation(m)","startDate", "endDate", "lapStart", "lapEnd", "numOverLap", "numObservation", "numOfMissing", "meanAP", "yearUsed", "TRMMUsedMAP", "TRMMAllMAP"]
myWriter.writerow(row)

for station in dataSpanish:
    row = []
    #row.append(station.stationName)
    row.append(station.fileName)
    row.append(station.mapId)
    row.append(station.lat)
    row.append(station.lon)
    row.append(station.elevation)
    row.append(station.dateList[0])
    row.append(station.dateList[-1])
    row.append(station.lapStart)
    row.append(station.lapEnd)
    row.append(station.numOverlap)
    row.append(station.numObservation)
    row.append(station.numOfMissing)
    row.append(station.meanAP)
    row.append(station.yearUsed)
    row.append(station.TRMMUsedMAP)
    row.append(station.TRMMAllMAP)
    #row.append(isRain)

    myWriter.writerow(row)





myHandler.close()










