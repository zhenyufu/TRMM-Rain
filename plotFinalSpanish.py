from rain import *
# load everything in plot/
# season1: dryTRMM, drySpanish, wetTRMM, wetSpanish
f1 = "plot/mapSpanish1"
data1 = pickle.load( open(f1, 'rb') )

fig = plt.figure(figsize=(16, 10))

titleSize = 20
labelSize = 20
plt.tick_params(labelsize = 14)
#################################3

popt, pcov, r_squared = plotAOverB(data1[0], data1[1], True, "Blue", "SENAMHI")


a1 = format(popt[0], '.2f')
b1 = format(popt[1], '.2f')
r1 = format(r_squared, '.2f')


title = "Annual Fit with SENAMHI and Atrium stations: " +  r'$y=' +  a1 + " x^{" + b1 + "}"  + "\/\/ r^2 = " + r1 + '$'

fig.suptitle(title, fontsize= titleSize)
plt.xlabel('Mean annual precipitation of weather stations (mm)', fontsize= labelSize )
plt.ylabel("Mean annual precipitation ratio (TRMM / WS)" , fontsize= labelSize )
plt.xlim(xmin=0)


print len(data1[0])


aDiv = [float(ai)/bi for ai,bi in zip(data1[0][-3:], data1[1][-3:])]
plt.scatter(data1[1][-3:], aDiv ,c= "magenta", label="Atrium", s= 36)




plt.legend(loc='upper right')



#################################3

plt.show()






