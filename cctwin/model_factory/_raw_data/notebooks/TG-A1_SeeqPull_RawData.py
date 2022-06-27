from urllib.request import CacheFTPHandler
from seeq import spy
import pandas as pd
import datetime
from pytz import timezone

spy.login(url='https://norte3.seeq.site/', access_key='bbB8vkfiSeGRBWPhp-lcXg', password='a3bdpagp31SBaR5JFRMSV1mGFle0xg')

print("\n******Getting TG-A1 Base Load and Part Load Data******\n")

#Copy and past the worksheet URL that contains all the sidnals you want
worksheet_url = 'https://norte3.seeq.site/workbook/E41272DC-2480-4B0E-9E27-A73C71C68BAA/worksheet/418D0EB3-56FC-411E-91A7-5CDDDA281A34'
#Search the worksheet and return the tags that are in the worksheet's detail pane
items = spy.search(worksheet_url,quiet=True)

#determine the time range for pulling the data
endtime =datetime.datetime.now(timezone('America/Chicago')) #current time
endtime.strftime('%m-%d-%y %H:%M:%S')

starttime = endtime - datetime.timedelta(days = 365) 
starttime.strftime('%m-%d-%y %H:%M:%S')

#pull data from Seeq return dataframe
df = spy.pull(items, start=starttime.strftime('%m-%d-%y %H:%M:%S'), end=endtime.strftime('%m-%d-%y %H:%M:%S'), errors='catalog', grid='15min', tz_convert='US/Central')

df.index.name="TimeStamp"

csv_file = "cctwin/model_factory/_raw_data/Norte3_TGA1_RawDataSeeq.csv"
df.to_csv(csv_file)

dfwithTimeStamp=pd.read_csv(csv_file, encoding="ISO-8859-2", low_memory=False)
cols=dfwithTimeStamp.columns.tolist()

gzip_file_name = "cctwin/model_factory/ctgs/model_data/Norte3_TGA1_RawDataSeeq.gzip"
dfwithTimeStamp.to_csv(gzip_file_name, encoding='ISO-8859-1', sep=',', index=False, compression="gzip")

print("\n****** TG-A1 Base Load and Part Load Data Collected! ******\n")

print("\n****** Getting TG-A1 Min Load 2x1 ******\n")

#Copy and past the worksheet URL that contains all the sidnals you want
worksheet_url = 'https://norte3.seeq.site/workbook/DB6404CD-1654-4D32-8E74-E338A41D2AB5/worksheet/765972E3-0994-4491-98A3-349DC4A5210B'

#Search the worksheet and return the tags that are in the worksheet's detail pane
items = spy.search(worksheet_url, quiet=True)

#Dropping those items that are not needed
items=items.drop([0, 3, 4])

#pull data from Seeq return dataframe
df = spy.pull(items, start=starttime.strftime('%m-%d-%y %H:%M:%S'), end=endtime.strftime('%m-%d-%y %H:%M:%S'), errors='catalog', grid='auto', tz_convert='US/Central')
df.index.name="TimeStamp"

store_df=df[df['Min Load & 2x1']==1]
store_df=store_df.drop(columns=['Min Load & 2x1'])

#Export the file as csv
store_df.to_csv('cctwin/model_factory/ctgs/model_data/Norte3_TGA1_MinLoad2x1.csv', index=False)

print("\n****** Getting TG-A1 Min Load 2x1 Data Collected! ******\n")

print("\n****** Getting TG-A1 Min Load 1x1 ******\n")

#Copy and past the worksheet URL that contains all the sidnals you want
worksheet_url = 'https://norte3.seeq.site/workbook/DB6404CD-1654-4D32-8E74-E338A41D2AB5/worksheet/853BB261-BD5C-45DA-A1CB-1D9CC15C51DD'

#Search the worksheet and return the tags that are in the worksheet's detail pane
items = spy.search(worksheet_url, quiet=True)

#Dropping those items that are not needed
items=items.drop([0, 3, 4])

#pull data from Seeq return dataframe
df = spy.pull(items, start=starttime.strftime('%m-%d-%y %H:%M:%S'), end=endtime.strftime('%m-%d-%y %H:%M:%S'), errors='catalog', grid='auto', tz_convert='US/Central')
df.index.name="TimeStamp"

store_df=df[df['Min Load 1x1']==1]
store_df=store_df.drop(columns=['Min Load 1x1'])

#Export the file as csv
store_df.to_csv('cctwin/model_factory/ctgs/model_data/Norte3_TGA1_MinLoad1x1.csv', index=False)

print("\n****** TG-A1 Min Load 1x1 Data Collected ******\n")