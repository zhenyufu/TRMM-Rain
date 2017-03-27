from rain import *

filePath = "raw_atrium/"
newFile = "_data/dataAtrium_0.1"


dataArray = []
temp =  sorted(glob.glob(filePath+ "*.tab"))

for p in temp:
# the for loop
#p = temp[0]
    f = open(p, 'rb')
    c = csv.reader(f, delimiter='\t')
    c = list(c) # pass in a list
    c = np.asarray(c)

    # remove the first header
    c = np.delete(c, 0)

    # remove the missing rows - the ones that don't have 6 or missing number on the 4
    iDelete = []
    for i in range (0, len(c)):
        if len(c[i]) != 6:
            iDelete.append(i)
        else:
            if c[i][4] == "":
                iDelete.append(i)

    c = np.delete(c, iDelete)

    # finished removing
    # retype
    c = list(c) # pass in a list
    c = np.asarray(c)

    stationData = StationData(c,p)
    dataArray.append(stationData)




# dump the array

out = open(newFile, 'wb')
pickle.dump(dataArray, out, pickle.HIGHEST_PROTOCOL)
out.close()

