from rain import *
# load everything in plot/
# season1: dryTRMM, drySpanish, wetTRMM, wetSpanish
f1 = "plot/mapSpanishOnly1"
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


title = "Annual Fit with SENAMHI stations: " +  r'$y=' +  a1 + " x^{" + b1 + "}"  + "\/\/ r^2 = " + r1 + '$'

fig.suptitle(title, fontsize= titleSize)
plt.xlabel('Mean annual precipitation of weather stations (mm)', fontsize= labelSize )
plt.ylabel("Mean annual precipitation ratio (TRMM / WS)" , fontsize= labelSize )
plt.xlim(xmin=0)





#################################3

plt.show()






