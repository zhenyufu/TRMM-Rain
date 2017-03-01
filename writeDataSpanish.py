from rain import *

oldFile = "_data/dataSpanish_0.4"
newFile = "_data/dataSpanish_0.99"

f = open(oldFile, 'rb')
dataSpanish = pickle.load(f)
out = open(newFile, 'wb')


# do shit in interactive consol and then
# pickle.dump(dataSpanish, out, pickle.HIGHEST_PROTOCOL)
# out.close()




# or after main.py
# out = open('_data/dataSpanish_0.99', 'wb')
# pickle.dump(dataSpanish, out, pickle.HIGHEST_PROTOCOL)
# out.close()
