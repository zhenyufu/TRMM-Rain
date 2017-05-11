from rain import *
# load everything in plot/
# season1: dryTRMM, drySpanish, wetTRMM, wetSpanish
f1 = "plot/check1"
data1 = pickle.load( open(f1, 'rb') )

fig = plt.figure(figsize=(16, 10))

titleSize = 20
labelSize = 20
plt.tick_params(labelsize = 14)
#################################3

xx = data1[0]
yy = data1[1]
plt.scatter(xx, yy, c= "blue", s= 36)


title = "Accuracy of corrected TRMM at Weather Stations"

fig.suptitle(title, fontsize= titleSize)
plt.xlabel('Corrected TRMM MAP (mm)', fontsize= labelSize )
plt.ylabel("Actual MAP (mm)" , fontsize= labelSize )
plt.xlim([0,20000])
plt.ylim([0,20000])




for i in range(0, len(xx)):
    print xx[i], ",", yy[i]

#################################3

plt.show()






