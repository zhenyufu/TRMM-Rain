from rain import *
# load everything in plot/
# season1: dryTRMM, drySpanish, wetTRMM, wetSpanish
f1 = "plot/elevation1"
data1 = pickle.load( open(f1, 'rb') )

fig = plt.figure(figsize=(16, 10))

titleSize = 20
labelSize = 20
plt.tick_params(labelsize = 14)
#################################3
a = data1[0]
b = data1[1]
ele = data1[2]



fdiv = [float(ai)/bi for ai,bi in zip(a,b)]
plt.scatter(ele, fdiv, c= "blue",s =36)


title = "TRMM MAP accuracy with change in elevation"

fig.suptitle(title, fontsize= titleSize)
plt.xlabel( "Elevation (m)", fontsize= labelSize )
plt.ylabel( "Mean annual precipitation ratio (TRMM / WS)"  , fontsize= labelSize )
plt.xlim(xmin=0)





#################################3

plt.show()






