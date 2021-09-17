# * * * * * * * * * * * * * * * * * * * * * * * *
# * The script aims to modify some informations *
# * on a given set of AP in a Meraki network.   *
# * * * * * * * * * * * * * * * * * * * * * * * *

import pandas as pd
import meraki
import sys
import time
from datetime import datetime

API_KEY = 'API_KEY'
dashboard = meraki.DashboardAPI(API_KEY)

# import excel file with informations
xlsx_dataframe = pd.read_excel (r'Informations_File.xlsx')
xlsx_dict = xlsx_dataframe.to_dict(orient='records')

index = 0

nameAP = input("+ Do you want to change NAMES? [y/n] ")
tagAP = input("+ Do you want to change TAGS? [y/n] ")

now = datetime.now()
start = now.strftime('%Y-%m-%d_%H-%M-%S')

for i in xlsx_dict: # i prende il valore della riga da 0 a fine-1 di xlsx_dict

    if nameAP=='y' and tagAP=='n':
        response = dashboard.devices.getDevice(
            i['serial']
        )
        if response['name']!=i['hostname']:
            print('-',response['serial'], 'old name',response['name'])
            response = dashboard.devices.updateDevice(
                i['serial'],
                name = i['hostname'],
                )
        else: 
            print('-',response['serial'], 'name',response['name'],'no change needed')
    
    else:
        conftag = i['tags'].split(',')
        if nameAP=='n' and tagAP=='y':
            response = dashboard.devices.updateDevice(
            i["serial"],
            tags = conftag
            )
        else:
            if nameAP=='y' and tagAP=='y':
                response = dashboard.devices.getDevice(
                    i['serial']
                )
                print('-',response['serial'], 'old name',response['name'])
                response = dashboard.devices.updateDevice(
                    i["serial"],
                    name = i['hostname'],
                    tags = conftag
                )

    print('-',response['serial'], 'name',response['name'])
    index=index+1
    print('\n- Progress:',index,'of',len(xlsx_dict),'-',str(int((index/len(xlsx_dict))*100)),'%')

now = datetime.now()
end = now.strftime('%Y-%m-%d_%H-%M-%S')

print('\n*** Process started at',start,'and completed at',end,'***\n')
