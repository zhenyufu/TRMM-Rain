from rain import *
# load everything in plot/
# season1: dryTRMM, drySpanish, wetTRMM, wetSpanish
f1 = "_data/dataSpanish_0.8.7"
data1 = pickle.load( open(f1, 'rb') )

# .6 is buggy remove the last 4
data1 = data1[:-4]
fig = plt.figure(figsize=(16, 10))

titleSize = 20
labelSize = 20
plt.tick_params(labelsize = 14)
#################################3

#for station in data1:
#    print station.stationName , station.TRMMUsedMAP , station.TRMMAllMAP
a = []
b = []

for i in range(0,len(data1)):
    if data1[i].TRMMUsedMAP != 0 and not Math.isnan(data1[i].TRMMUsedMAP):
        print data1[i].TRMMUsedMAP
        a.append (data1[i].TRMMUsedMAP)
        b.append (data1[i].TRMMAllMAP)
        #data1[i]
    #print station.stationName , station.TRMMUsedMAP , station.TRMMAllMAP

print a
print b
plt.scatter(a, b, c= "blue",s =36)
a = np.asarray(a)
b = np.asarray(b)
popt, pcov = curve_fit(curveLinear, a, b)
xx = np.linspace(0.1, 5500, 100)
yy = curveLinear(xx, *popt)
plt.plot(xx,yy, c="blue")

residuals = b - curveLinear(a, popt[0], popt[1])
ss_res = np.sum(residuals**2)
ss_tot = np.sum((b-np.mean(b))**2)
r = 1 - (ss_res / ss_tot)

a1 = format(popt[0], '.2f')
b1 = format(popt[1], '.2f')

r = format(r, '.2f')

title = "SENAMHI and Atrium Station's TRMM overlap period as representation of total TRMM record\n"
title += r'$y=' +  a1 + " x " + b1 + ""  + "\/\/ r^2 = " + r + '$'

fig.suptitle(title, fontsize= titleSize)
plt.xlabel( "Overlap period TRMM MAP (mm)", fontsize= labelSize )
plt.ylabel( "All TRMM temporal record MAP (mm)"  , fontsize= labelSize )
plt.xlim([0,5500])
plt.ylim([0,5500])

# can only see 9 points cause 1523.9692356482149 and 1525.2538505360485 basically overlap


#################################3

plt.show()






