from rain import *

proj = "mill" # "stere"
cFile = "_data/dataCorrelation_0.1"
imageDir = "img/"
imagePre = "rain"
imageSave = True
imageShow = False
doCorrection = True


f = open(cFile, 'rb')
dataCorrelation = pickle.load(f)
dataTRMM ,TRMMDateList = readTRMM("../TRMM_3B42_Daily.1998-2016.7.SouthAmerica.nc")
print "finished data reading"
if imageShow:
    plt.ion()

# get the lat lon array as they are the same
latArray = dataTRMM.variables['lat'][:]
lonArray = dataTRMM.variables['lon'][:]



def doDrawRain(i):
    #prepArray = dataTRMM.variables['precipitation'][1,:,:];
    myDate = TRMMDateList[i]
    prepArray = dataTRMM.variables['precipitation'][i,:,:]
    nx = prepArray.shape[0]
    ny = prepArray.shape[1]

    # create figure and axes instances
    fig = plt.figure(figsize=(8,8))
    #ax = fig.add_axes([0.1,0.1,0.8,0.8])

    # apply correlation correction
    # dry season
    imageSeason = ""
    iSeason = -1
    if isDrySeason(myDate.month):
        iSeason = 0
        imageSeason = "dry"
    else:
        iSeason = 1
        imageSeason = "wet"

    # correction
    if doCorrection:
        #plot the original

        popt = dataCorrelation[iSeason].popt
        a = popt[0]
        b = popt[1]
        prepArray = ((prepArray[:]) / a )**(1/(b+1))

        #ax = fig.add_subplot(121)
        #ax.set_title('original')




    # setup basemap.
    m = Basemap(projection= proj, lat_0=-14.475, lon_0=-72.126,\
                llcrnrlat=latArray[0],urcrnrlat=latArray[-1],\
                llcrnrlon=lonArray[0],urcrnrlon=lonArray[-1],\
                resolution='l')

    m.drawcoastlines()
    m.drawcountries()
    m.drawparallels(np.arange(-90,90,10),labels=[1,0,0,0],fontsize=10)
    m.drawmeridians(np.arange(0,360,10),labels=[0,0,0,1],fontsize=10)




    # start drawing
    lons, lats = m.makegrid(nx, ny)# get lat/lons of ny by nx evenly space grid.
    x, y  = m(lons, lats)# compute map proj coordinates.
    # draw filled contours.
    clevs = [0,1,2.5,5,7.5,10,15,20,30,40,50,70,100,150,200,250,300,400,500,600,750]

    #m.scatter(x, y, marker='o')


    cs = m.contourf(x,y,prepArray.T,clevs,cmap=cm.s3pcpn) # prepArray.T as the lat lon is annoyingly switched in the TRMM data!!
    cbar = m.colorbar(cs,location='bottom',pad="5%")
    cbar.set_label('mm')

    #########################
    print "Finished:" , str(myDate)
    plt.title("Hi: " +  str(myDate) + " - season: "+ imageSeason)

    if imageShow:
        plt.show()
    if imageSave:
        plt.savefig(imageDir + imagePre + "_" + str(i).zfill(4)  + "_" + str(myDate) + "_" + imageSeason + ".png")
        plt.close(fig)






for i in range (0, len(dataTRMM.variables['precipitation'])):
   doDrawRain(i)




