from numpy import *
import os,sys
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

(size, files, percent)=stats(df)

#-----------
# End
#-----------
print('Collection in variable: df')

save_and_backup(df)
