#downloads inventory feed and uploads relevant data to google cloud -> drive -> sheets to be used in google ads dynamic page feed

#imports needed libraries
#dom.sh downloads an inventory csv file from an ftp server
#requires credentials json file 

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os

#downloads file from ftp
os.system('bash ~/ads/dominion/dom.sh')

#reads and transforms file
file1 = pd.read_csv('dominv.csv', index=False)
frame1 = file1[['Final URL', 'Item title']]
frame1['Custom label'] = frame1['Item title']
frame1['Page URL'] = frame1['Final URL']
frame2 = frame1[['Page URL','Custom label']]
frame2.to_csv('dpf.csv', index=False)

#define scope and credentials for google cloud
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(credentials)

#opens google sheets spreadsheet and writes file to spreadsheet
spreadsheet = client.open('Google Ads - Dynamic Page Feed')
with open('dpf.csv', 'r') as file_obj:
    content = file_obj.read()
    client.import_csv(spreadsheet.id, data=content)
