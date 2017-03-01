from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np


# setup Lambert Conformal basemap.
m = Basemap(width=3000000,height=3000000,projection='lcc',
            resolution='l',lat_0=-14.475,lon_0=-72.126)
m.bluemarble()

#m.drawcoastlines()
m.drawcountries()
#m.drawmapboundary(fill_color='aqua')
#m.fillcontinents(color='coral',lake_color='aqua')

m.drawmeridians(np.arange(0,360,10))
m.drawparallels(np.arange(-90,90,10))
plt.show()

