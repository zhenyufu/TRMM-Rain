from rain import *

def getIndex(tempList):
    position = 0
    myList = []
    #tempList = list(tempList)

    for i in tempList: #np.nditer(tempList):
        #print "starting type", type(i), "of value", i
        #print "*",i,"*"
        try:
            x = i.astype(np.float)
            #x= float(i)
        except Exception as e:
            #print "at index", str(position), "of list", tempList, "with erro:", str(e)
            #print "*",i,"*"
            #raw_input("Press Enter to continue...") #print"type" , type(x)
            myList.append(position)
            position += 1
            continue
        if x < 0:
            myList.append(position)
        position += 1
    return myList


oldFile = "_data/dataSpanish_0.8"
newFile = "_data/dataSpanish_0.8.1"

f = open(oldFile, 'rb')
dataSpanish = pickle.load(f)


path = "raw_senamhi/"
temp =  sorted(glob.glob(path + "*.csv"))
iFile = 0
for p in temp:
    ff = open(p, 'rb')
    c = csv.reader(ff, delimiter=',')
    c = list(c) # pass in a list
    tempArray = np.asarray(c)
    tempCol = tempArray.shape[1]

    print "processing" , p, "which has col " , tempCol
    problemIndex = []

    #print tempArray[:,9]
    if tempCol == 13:
        print "first"
        problemIndex = getIndex(tempArray[:,9])
        print "second"
        problemIndex.extend(getIndex(tempArray[:,10]))
    elif tempCol == 9:
        problemIndex = getIndex(tempArray[:,5])
    elif tempCol ==3:
        problemIndex = getIndex(tempArray[:,1])
        problemIndex.extend(getIndex(tempArray[:,2]))
    print "has problem index" , problemIndex

    for i in problemIndex:
        s = dataSpanish[iFile]
        print s.fileName , "has index" , i, "wrong with" , s.listPrep[i]
        #raw_input("Press Enter to continue...")
        s.listPrep[i] = -999
    print "**************"
    iFile +=1



out = open(newFile, 'wb')
pickle.dump(dataSpanish, out, pickle.HIGHEST_PROTOCOL)
out.close()











