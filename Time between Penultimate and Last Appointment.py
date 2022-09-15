import pandas as pd
import os
import datetime as dt
import numpy as np
os.chdir(r'M:\MSG Open Episodes\Apointments pull 24.01.22')

"""
A program that returns the number of days between the penultimate and last appointment within an episode of care

"""

# import all appointments
df = pd.read_csv('apptsFull.txt', '\t')

# define column headers 
df.columns=['URN', 'EpisodeNumber', 'CareProvider', 'Speciality', 'Unknown', 'AppointmentDate', 'AppointmentTime', 'AptCareProvider', 'AptSpeciality', 'Group']

# change column headers
cols = list(df.columns)

# ensure that all dates to be processed are in DT format
df['AppointmentDate'] =  pd.to_datetime(df['AppointmentDate'],errors='coerce')

# sort values
df = df.sort_values(['URN','EpisodeNumber','AppointmentDate', 'AppointmentTime'],ascending=[True,False,False,False])

# group data into episodes of care
ep_groups = df.groupby('EpisodeNumber')

results_list = []
for k,v in ep_groups:
    # define penultimate appointment date within episode of care
    v['PreviousApt'] = v['AppointmentDate'].shift(-1)
    # calculate date difference
    v['DaysSincePrivousAppiontment'] = v['AppointmentDate'] -  v['PreviousApt']
    # append group (episode of care) to results list
    df_out = v
    results_list.append(df_out)

# results list to DataFrame    
df_res =  pd.concat(results_list)

# convery into standard units
df_res['DaysSincePrivousAppiontment'] = df_res['DaysSincePrivousAppiontment'].dt.total_seconds()
df_res['DaysSincePrivousAppiontment'] = df_res['DaysSincePrivousAppiontment'] / 60 / 60 / 24

# define threshold in years and results DataFrame
years = 10
number_days = years*365
df_res = df_res[df_res['DaysSincePrivousAppiontment'] > number_days]

# export to excel
df_res.to_excel('Days between appointments.xlsx', index= False)
