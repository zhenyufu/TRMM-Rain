from rain import *

f = open('_data/dataSpanish_0.8.4', 'rb')
dataSpanish = pickle.load(f)

proj = "mill"






fig = plt.figure(figsize=(8,8))








m = Basemap(projection= proj, lat_0=-14.475, lon_0=-72.126,\
                  llcrnrlat=-18.62,urcrnrlat=-9.32, \
                  llcrnrlon=-76.61 ,urcrnrlon=-66.41, \
                  resolution='l')


m.drawcoastlines()
m.drawcountries()
#m.drawrivers(linewidth=0.5, linestyle='solid', color='blue')
m.drawparallels(np.arange(-90,90,1),labels=[1,0,0,0],fontsize=10)
m.drawmeridians(np.arange(0,360,1),labels=[0,0,0,1],fontsize=10)


for station in dataSpanish:
    print station.stationName , station.lat , station.lon

    lon = float(station.lon)
    lat = float(station.lat)
    x,y = m(lon, lat)
    m.plot(x, y, 'ro', markersize=8)

fig.suptitle("Weather Stations: SENAMHI and Atrium", fontsize= 20)

plt.show()



