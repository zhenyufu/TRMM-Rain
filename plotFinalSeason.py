from rain import *
# load everything in plot/
# season1: dryTRMM, drySpanish, wetTRMM, wetSpanish
f1 = "plot/season1"
data1 = pickle.load( open(f1, 'rb') )

fig = plt.figure(figsize=(16, 10))

titleSize = 20
labelSize = 20
plt.tick_params(labelsize = 14)
#################################3

popt, pcov, r_squared = plotAOverB(data1[0], data1[1], True, "red", "Dry Season")
popt2, pcov2, r_squared2 = plotAOverB(data1[2], data1[3], True, "blue", "Wet Season")


a1 = format(popt[0], '.2f')
b1 = format(popt[1], '.2f')
r1 = format(r_squared, '.2f')
a2 = format(popt2[0], '.2f')
b2 = format(popt2[1], '.2f')
r2 = format(r_squared2, '.2f')




title = "Dry Season Fit: " +  r'$y=' +  a1 + " x^{" + b1 + "}"  + "\/\/ r^2 = " + r1 + '$'
title += "\n"
title += "Wet Season Fit: " +  r'$y=' +  a2 + " x^{" + b2 + "}"  + "\/\/ r^2 = " + r2 + '$'

fig.suptitle(title, fontsize= titleSize)
plt.xlabel('Mean seasonal precipitation of weather stations (mm)', fontsize= labelSize )
plt.ylabel("Mean seasonal precipitation ratio (TRMM / WS)" , fontsize= labelSize )
plt.legend(loc='upper right')
plt.xlim(xmin=0)




#################################3

plt.show()






