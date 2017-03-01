import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# generate some data with noise
xData = np.linspace(0.01, 100., 50)
aOrg = 0.08
Norg = 10.5
yData = Norg * xData ** (-aOrg) + np.random.normal(0, 0.5, len(xData))
xData = xData *10

# get logarithmic data
lx = np.log(xData)
ly = np.log(yData)

def f(x, N, a):
    return N * x ** (-a)

def f_log(x, lN, a):
    return a * x + lN

# optimize using the appropriate bounds
popt, pcov = curve_fit(f, xData, yData)
popt_log, pcov_log = curve_fit(f_log, lx, ly)

xnew = np.linspace(0.01, 100., 5000)

# plot the data
plt.plot(xData, yData, 'bo')
plt.plot(xnew, f(xnew, *popt), 'r')
plt.plot(xnew, f(xnew, np.exp(popt_log[0]), -popt_log[1]), 'k')
plt.show()

