from rain import *

proj = "mill" # "stere"
cFile = "_data/dataCorrelation_0.4"
imageDir = "img/"
imagePre = "rain"
imageSave = True
imageShow = False
doCorrection = True
withFocus = True

aFile = "_data/dataAnnualRatio_0.2"
fa = open(aFile, 'rb')
ratioList  = pickle.load(fa)
ratioDry =  ratioList[0]
ratioWet =  ratioList[1]

f = open(cFile, 'rb')
dataCorrelation = pickle.load(f)
dataTRMM ,TRMMDateList = readTRMM("../TRMM_3B42_Daily.1998-2016.7.SouthAmerica.nc")
print "finished data reading"
print "Using dry" , dataCorrelation[0].popt
print "Using wet" , dataCorrelation[1].popt


if imageShow:
    plt.ion()

# get the lat lon array as they are the same
latArray = dataTRMM.variables['lat'][:]
lonArray = dataTRMM.variables['lon'][:]

def doSubplot(fig, prepArray, myDate, pid, pName):
    ax = fig.add_subplot(pid)
    ax.set_title(pName)
    nx = prepArray.shape[0]
    ny = prepArray.shape[1]


    # setup basemap.
    if withFocus:
        m = Basemap(projection= proj, lat_0=-14.475, lon_0=-72.126,\
                 llcrnrlat=-18.62,urcrnrlat=-9.32, \
                 llcrnrlon=-76.61 ,urcrnrlon=-66.41, \
                 resolution='l')
    else:
        m = Basemap(projection= proj, lat_0=-14.475, lon_0=-72.126,\
                llcrnrlat=latArray[0],urcrnrlat=latArray[-1],\
                llcrnrlon=lonArray[0],urcrnrlon=lonArray[-1],\
                resolution='l')

    m.drawcoastlines()
    m.drawcountries()
    m.drawparallels(np.arange(-90,90,1),labels=[1,0,0,0],fontsize=10)
    m.drawmeridians(np.arange(0,360,1),labels=[0,0,0,1],fontsize=10)
    # 1 for closeup, 10 for



    # start drawing
    lons, lats = m.makegrid(nx, ny)# get lat/lons of ny by nx evenly space grid.
    x, y  = m(lons, lats)# compute map proj coordinates.
    # draw filled contours.
    clevs = [0,1,2.5,5,7.5,10,15,20,30,40,50,70,100,150,200,250,300,400,500,600,750]

    #m.scatter(x, y, marker='o')


    cs = m.contourf(x,y,prepArray.T,clevs,cmap=cm.s3pcpn) # prepArray.T as the lat lon is annoyingly switched in the TRMM data!!
    cbar = m.colorbar(cs,location='bottom',pad="5%")
    cbar.set_label('mm')





def doDrawRain(i):
    myDate = TRMMDateList[i]
    prepArray = dataTRMM.variables['precipitation'][i,:,:]


    # create figure and axes instances
    if withFocus:
        fig = plt.figure(figsize=(16,12))
    else:
        fig = plt.figure(figsize=(8,8))
    doSubplot(fig, prepArray, myDate, 121,"Original")


    # apply correlation correction
    # dry season
    imageSeason = ""
    iSeason = -1
    if isDrySeason(myDate.month) == 1:
        iSeason = 0
        imageSeason = "dry"
        prepArray = prepArray * ratioDry
    else:
        iSeason = 1
        imageSeason = "wet"
        prepArray = prepArray * ratioWet
    # correction
    if doCorrection:
        #plot the original

        #popt = dataCorrelation[iSeason].popt
        #print popt
        #a = popt[0]
        #b = popt[1]
        #prepArray = ((prepArray[:])/ a )**(1/(b+1))
        #prepArray = prepArray * ratioDry

        doSubplot(fig, prepArray, myDate, 122, "Corrected")


    #########################
    print "Finished:" , str(myDate)
    fig.suptitle("Daily Precipitation map: " +  str(myDate) + " - season: "+ imageSeason)

    if imageShow:
        plt.show()
    if imageSave:
        plt.savefig(imageDir + imagePre + "_" + str(i).zfill(4)  + "_" + str(myDate) + "_" + imageSeason + ".png")
        plt.close(fig)






for i in range (0, len(dataTRMM.variables['precipitation'])):
   doDrawRain(i)




