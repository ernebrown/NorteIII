from urllib.request import CacheFTPHandler
from seeq import spy
import pandas as pd
import datetime
from pytz import timezone

spy.login(url='https://norte3.seeq.site/', access_key='bbB8vkfiSeGRBWPhp-lcXg', password='a3bdpagp31SBaR5JFRMSV1mGFle0xg')

print("\n******Getting TG-A2 Base Load and Part Load Data******\n")

#Copy and past the worksheet URL that contains all the signals you want
worksheet_url = 'https://norte3.seeq.site/workbook/E41272DC-2480-4B0E-9E27-A73C71C68BAA/worksheet/A02EC1AD-AD0E-4F9E-A824-7D5C3B8F3ABE'
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

csv_file = "cctwin/model_factory/_raw_data/Norte3_TGA2_RawDataSeeq.csv"
df.to_csv(csv_file)

dfwithTimeStamp=pd.read_csv(csv_file, encoding="ISO-8859-2", low_memory=False)
cols=dfwithTimeStamp.columns.tolist()

gzip_file_name = "cctwin/model_factory/ctgs/model_data/Norte3_TGA2_RawDataSeeq.gzip"
dfwithTimeStamp.to_csv(gzip_file_name, encoding='ISO-8859-1', sep=',', index=False, compression="gzip")

print("\n****** TG-A2 Base Load and Part Load Data Collected! ******\n")

print("\n****** Getting TG-A2 Min Load 2x1 ******\n")

#Copy and past the worksheet URL that contains all the signals you want
worksheet_url = 'https://norte3.seeq.site/workbook/DB6404CD-1654-4D32-8E74-E338A41D2AB5/worksheet/DF621CFF-30AB-4F88-8435-0CB8C39A4277'

#Search the worksheet and return the tags that are in the worksheet's detail pane
items = spy.search(worksheet_url, quiet=True)

#Dropping those items that are not needed
items=items.drop([0, 3, 4])

#pull data from Seeq return dataframe
df = spy.pull(items, start=starttime.strftime('%m-%d-%y %H:%M:%S'), end=endtime.strftime('%m-%d-%y %H:%M:%S'), errors='catalog', grid='auto', tz_convert='US/Central')
df.index.name="TimeStamp"

store_df=df[df['TG-A2 Min Load 2x1']==1]
store_df=store_df.drop(columns=['TG-A2 Min Load 2x1'])

#Export the file as csv
store_df.to_csv('cctwin/model_factory/ctgs/model_data/Norte3_TGA2_MinLoad2x1.csv', index=False)

print("\n****** TG-A2 Min Load 2x1 Data Collected! ******\n")

print("\n****** Getting TG-A2 Min Load 1x1 ******\n")

#Copy and past the worksheet URL that contains all the sidnals you want
worksheet_url = 'https://norte3.seeq.site/workbook/DB6404CD-1654-4D32-8E74-E338A41D2AB5/worksheet/032A9AFC-75A2-40B8-AFEF-3E7D5C5BB73F'

#Search the worksheet and return the tags that are in the worksheet's detail pane
items = spy.search(worksheet_url, quiet=True)

#Dropping those items that are not needed
items=items.drop([0, 3, 4])

#pull data from Seeq return dataframe
df = spy.pull(items, start=starttime.strftime('%m-%d-%y %H:%M:%S'), end=endtime.strftime('%m-%d-%y %H:%M:%S'), errors='catalog', grid='auto', tz_convert='US/Central')
df.index.name="TimeStamp"

store_df=df[df['TG-A2 Min Load 1x1']==1]
store_df=store_df.drop(columns=['TG-A2 Min Load 1x1'])

#Export the file as csv
store_df.to_csv('cctwin/model_factory/ctgs/model_data/Norte3_TGA2_MinLoad1x1.csv', index=False)

print("\n****** TG-A2 Min Load 1x1 Data Collected! ******\n")