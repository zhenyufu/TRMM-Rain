from rain import *
isCheck = True

if isCheck:
    aFile = "_data/dataAnnualRatio_0.2"
    fa = open(aFile, 'rb')
    ratioList  = pickle.load(fa)
    ratioDry =  ratioList[0]
    ratioWet =  ratioList[1]



# python -i -W ignore writeSeasonRatio.py
dataTRMM ,TRMMDateList = readTRMM("../TRMM_3B42_Daily.1998-2016.7.SouthAmerica.nc")
# 1998/1/1 datetime.date(2016, 10, 30)
yearLength = 2016 - 1998

cFile = "_data/dataCorrelation_0.4"
aFile = "_data/dataAnnualRatio_0.2"



f = open(cFile, 'rb')
dataCorrelation = pickle.load(f)
dryC =  dataCorrelation[0]
wetC = dataCorrelation[1]

a1 = dryC.popt[0].item()
b1 = dryC.popt[1].item()
a2 = wetC.popt[0].item()
b2 = wetC.popt[1].item()
list1 = []
list2 = []
if isCheck:
    list3 = []
    list4 = []

prepArray = dataTRMM.variables['precipitation'][:,:,:]


#dataTRMMMAP = np.zeros((prepArray.shape[1] , prepArray.shape[2] )); #
#allMAP = np.zeros((yearLength , prepArray.shape[1] , prepArray.shape[2] )); #
temp = np.zeros((prepArray.shape[1] , prepArray.shape[2] )); # using for cumulating
if isCheck:
    temp3 = np.zeros((prepArray.shape[1] , prepArray.shape[2] ));
    temp4 = np.zeros((prepArray.shape[1] , prepArray.shape[2] ));


dayCounter = TRMMDateList[0]
endDay = datetime.date(2016,10,30) #TRMMDateList[-1]
while not(dayCounter.month == 5 or dayCounter.month == 11):
    dayCounter += datetime.timedelta(days=1)

print "counting  starts:", dayCounter


i = 0
year = 0

while (dayCounter <= endDay):
    seasonId = isDrySeason(dayCounter.month)
    if seasonId == -1:
        print "seaons count messed up"
        dayCounter += datetime.timedelta(days=1)
        continue

    print "season start:", dayCounter
    while isDrySeason(dayCounter.month) ==  seasonId:
        if isCheck:
            if isDrySeason(dayCounter.month) == 1:
                #temp += np.multiply(prepArray[i,:,:],ratioDry)
                temp3 += prepArray[i,:,:]*ratioDry
            else:
                #temp += np.multiply(prepArray[i,:,:],ratioWet)
                temp4 += prepArray[i,:,:]*ratioWet
        #else:
        temp += prepArray[i,:,:]

        dayCounter += datetime.timedelta(days=1)
        i += 1
    # comes out of a season
    if isDrySeason(dayCounter.month) == 1: # was just in wet 2
        list2.append(temp)
        if isCheck:
            list4.append(temp4)
    if isDrySeason(dayCounter.month) == 2: # was just in dry 1
        list1.append(temp)
        if isCheck:
            list3.append(temp3)

    temp = np.zeros((prepArray.shape[1] , prepArray.shape[2] ));
    if isCheck:
        temp3 = np.zeros((prepArray.shape[1] , prepArray.shape[2] ));
        temp4 = np.zeros((prepArray.shape[1] , prepArray.shape[2] ));






####### finished in loops
print "dry 1  length", len(list1)
print "wet 2  length", len(list2)
dataMap1 = np.mean(list1, axis = 0)
dataMap2 = np.mean(list2, axis = 0)



if isCheck:
    print "only  checking, not writing"
    dataMap3 = np.mean(list3, axis = 0)
    dataMap4 = np.mean(list4, axis = 0)
    print "dry 3  length", len(list3)
    print "wet 4  length", len(list4)

    fig = plt.figure()
    popt, pcov, r_squared = plotAOverB(dataMap1.ravel().tolist(), dataMap3.ravel().tolist(), True, "blue", "dry")
    popt2, pcov2, r_squared2 = plotAOverB(dataMap2.ravel().tolist(), dataMap4.ravel().tolist(), True, "red", "wet")

    pre = ""
    title =""
    pre+= "bySeason - Dry: "
    title = pre + "y=" + str(popt[0]) + " x^(" + str(popt[1]) + ")" + "\n      Rsqrt: " + str(r_squared)
    title +=  "\n Wet: y=" + str(popt2[0]) + " x^(" + str(popt2[1]) + ")" +          "\n      Rsqrt: " + str(r_squared2)


    fig.suptitle( title, fontsize=20)
    plt.xlabel('corrected')
    plt.ylabel("original/corrected")
    plt.legend(loc='upper right')

    plt.show()


else:
    ## correction
    corrected1 = ((dataMap1)/ a1 )**(1/(b1+1))
    corrected2 = ((dataMap2)/ a2 )**(1/(b2+1))


    dataRatio1 = corrected1 / dataMap1
    dataRatio2 = corrected2 / dataMap2

    ratioList = []
    ratioList.append(dataRatio1)
    ratioList.append(dataRatio2)

    ## output
    out = open(aFile, 'wb')
    pickle.dump(ratioList, out, pickle.HIGHEST_PROTOCOL)
    out.close()



