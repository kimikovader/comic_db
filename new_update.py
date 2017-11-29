import os,sys
from numpy import *
import pandas as pd
import datetime

import search_comics
import imp
imp.reload(search_comics)
from search_comics import *

'''This is code that updates the pandas DATAFRAME and .csv with the new Comics Data'''

#-----------------
# Background
#----------------

folder_name='/Users/ksakamoto/Desktop/Comics'
df=read_and_sort(folder_name)

old_data=load_comics('/Users/ksakamoto/Desktop/Comics/comics_db.csv')

#----------------------------------
# Difference between two dataframes
#----------------------------------

# File difference
if len(df)>=len(old_data):
	print('\nDetected ', len(df)-len(old_data), ' new files')
elif len(df)<len(old_data):
	print('\nRemoved ', len(old_data)-len(df), ' files')

print('\nUpdating DataFrame...')

# This makes sure the info from the .csv file is saved in the new dataframe
filt=where(df['File_name']==old_data['File_name'])[0]
filt2=where(old_data['File_name']==df['File_name'])[0]

df.loc[filt]=old_data.loc[filt2]

print('Done.\n')

#----------
# Stats
#----------

print('Files found: ', len(df), '\nTotal Size: ', round(df['Size'].sum()*10**(-3),2), 'GB')

ind=df.query('Read==1').index
file_num=len(ind)
size_tot=df.loc[ind,'Size'].sum()

print('Read: ', file_num, ' files or ', round(size_tot/df['Size'].sum()*100,2),'% of Comics')

#-----------
# End
#-----------
print('Collection in variable: df')

save_and_backup(df)
