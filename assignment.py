import requests
import pandas as pd
import io
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import datetime
import math

#number of days
numdays = int(input("Number of days? "))

#select country
cntrstr = 131     
cntrname = "India"      

#John Hopkins University CSSE raw data from Github repo (can change source if necessary)
jhuurl = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

#using GET method from requests library to make an HTTPS request to the JHU raw csv
jhudata = requests.get(jhuurl).content

#using Pandas and IO to read the CSV file format
ds = pd.read_csv(io.StringIO(jhudata.decode("utf-8")))


#setting a dataframe for the CSV file
df = pd.DataFrame(ds)

#accessing the last 29 days' data
res = df.loc[cntrstr].tolist()[-numdays:-1]

#appending latest data from a more updated server
wdurl = "https://www.worldometers.info/coronavirus/"
wddata = requests.get(wdurl)

#parsing webpage with BS4
soup = BeautifulSoup(wddata.text, "html.parser")
latest_number = soup.find("td", text=cntrname).find_next_sibling("td").text
lt2 = latest_number.replace(",", "")
res.append(int(lt2))

#logarithmic
for k in range(len(res)):
    res[k] = math.log(res[k])



#creating a list of dates
dtlist = []

for i in range(numdays):
    a = datetime.datetime.today() - datetime.timedelta(days=i)
    a = str(a.strftime("%d-%m-%Y"))
    dtlist.append(a)

dtlist.reverse()


#plot
plt.plot(dtlist, res)
plt.xlabel("Date")

plt.ylabel("Number of cases")
plt.title("COVID-19 cases in " + cntrname + " in last " + str(numdays) + " days")
plt.grid(True)


#plot formatting
if numdays <= 6:
    plt.xticks(rotation=0)
    
elif numdays > 6 and numdays < 13:
    plt.xticks(rotation=45)
    
elif numdays >= 13 and numdays < 19:    
    plt.xticks(rotation=90)
    
else:
    plt.xticks(rotation = 90)

#plot output
plt.show()