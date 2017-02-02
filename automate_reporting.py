from __future__ import print_function
import pandas as pd
import json
import os
from os import path
import to_sheets
from to_sheets import updatesheet

with open("../config_files/rp_mapping.json") as ft:
        mapping = json.load(ft)

with open('../config_files/services.json') as sf:
    services = json.load(sf)

services_list = list(services.keys())

def aggregate_automate(rpentity):
    return mapping[rpentity]

def get_date(date):
    full_timestamp = date[:date.find('T')]
    return full_timestamp

def get_verification_csvs(csvs,frequency):
    print('data_csvs/verification/'+frequency+'/'+csvs)
    df = pd.read_csv('../not_to_github/verification/'+frequency+'/'+csvs)
    df['RP name'] = df.apply(lambda row: aggregate_automate(row['RP Entity Id']),axis=1)
    
    df.index = pd.to_datetime(df['Timestamp'])
    
    return df
    
def verification_data():
    verification_weekly_csvs = os.listdir('../not_to_github/verification/weekly')

    if '.DS_Store' in verification_weekly_csvs:
        verification_weekly_csvs.remove('.DS_Store')


    weekly_resultdf = pd.DataFrame()

    verification_csvs = verification_weekly_csvs

    for csv in verification_csvs:
        weekly_resultdf = weekly_resultdf.append(get_verification_csvs(csv,'weekly'))

    weekly_resultdf.index = pd.to_datetime(weekly_resultdf['Timestamp'])
            
    return weekly_resultdf

def format_vf_df(df,type):
    services_list = list(services.keys())
    services_list.insert(0,'Timestamp')

    if type == 'new':
        df = df[df['Response type']=='NEW']
        df.fillna(0, inplace=True)
        df = df[services_list]
        # df = df[['Timestamp','DEFRA RP','DVLA VDL','DWP UCDS','HMRC CC','HMRC FF','HMRC PTA','HMRC SA','HMRC TE','HMRC YSP','DVLA F2D RENEW','DVLA F2D REPORT','BIS RP']]


    else:
        df = df[df['Response type']=='RETURNING']
        df.fillna(0, inplace=True)
        df = df[services_list]
        # df = df[['Timestamp','DEFRA RP','DVLA VDL','DWP UCDS','HMRC CC','HMRC FF','HMRC PTA','HMRC SA','HMRC TE','HMRC YSP','DVLA F2D RENEW','DVLA F2D REPORT','BIS RP']]
        
    return df

def totals(df):
    dfcolumns = list(df.columns)
    dfcolumns.remove('Timestamp')
    df['total'] = df[dfcolumns].sum(axis=1)
    return df['total']

def set_cols(df):
    df['total'] = totals(df)

    df = df[services_list]

    # df = df[['Timestamp','total','DEFRA RP','DVLA VDL','DWP UCDS','HMRC CC','HMRC FANDF','HMRC PTA','HMRC SA','HMRC TE','HMRC YSP','DVLA F2D RENEW','DVLA F2D REPORT','BIS RP']]

    return df

def get_final_df():
    
    weekly_resultdf = verification_data()
    weekly_resultdf = weekly_resultdf.groupby(['RP name','Response type']).resample('W-MON')['Response type'].count()
    weekly_resultdf = weekly_resultdf.unstack(level=0)
    print(weekly_resultdf.head())
    weekly_resultdf.reset_index(inplace=True)
    weekly_new_pivot = format_vf_df(weekly_resultdf,'new')
    # weekly_new_pivot = set_cols(weekly_new_pivot)
    weekly_new_pivot.reset_index(inplace=True)
    weekly_returning_pivot = format_vf_df(weekly_resultdf,'returning')
    # weekly_returning_pivot = set_cols(weekly_returning_pivot)
    weekly_returning_pivot.reset_index(inplace=True)


    return weekly_new_pivot, weekly_returning_pivot