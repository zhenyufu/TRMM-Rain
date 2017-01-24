import csv
import urllib2
from bs4 import BeautifulSoup


myLoc = "000691"
myFile = "madre4.csv"
myTipo = "CON" # red is CON, yellow is SUT

##############
myHandler = open(myFile,"a")
myWriter = csv.writer(myHandler)
myFind = "http://www.senamhi.gob.pe/include_mapas/_dat_esta_tipo.php?estaciones=" + myLoc

def getUrl(myTime):
    # return "http://www.senamhi.gob.pe/include_mapas/_dat_esta_tipo02.php?estaciones=" + myLoc + "&tipo=CON&CBOFiltro=" + myTime + "&t_e=M"
    return "http://www.senamhi.gob.pe/include_mapas/_dat_esta_tipo02.php?estaciones=" + myLoc + "&tipo=" + myTipo +"&CBOFiltro=" + myTime + "&t_e=M"


#### START
myMonth = []


# find the avaliable month first
page = urllib2.urlopen(myFind)
soup = BeautifulSoup(page.read())
options = soup.find("select", attrs={"class":"dire"}).find_all("option")
myMonth = [e.text.strip().encode('ascii') for e in options]


#remove all the -
for m in myMonth:
    m = m.replace("-", "")
    print m

    # for every month
    myUrl= getUrl(m)
    page = urllib2.urlopen(myUrl)
    soup = BeautifulSoup(page.read())
    table = soup.find("table", attrs={"class":"body01"})


    # rows = table.find_all('tr')
    rows = table.findAll("tr", {"bgcolor": None})
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        temp = [ele.encode('utf-8') for ele in cols]
        #print temp
        myWriter.writerow(temp)
#### END

myHandler.close()








