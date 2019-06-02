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

print('Updating Dataframe...')
folder_name='/Users/ksakamoto/Desktop/Comics/comics'
df=read_and_sort(folder_name)

old_data=load_comics('/Users/ksakamoto/Desktop/Comics/comics_db.csv')
deprecated_file=load_comics('/Users/ksakamoto/Desktop/Comics/dep_comics_db.csv')
#----------------------------------
# Difference between two dataframes
#----------------------------------
# This makes sure the info from the .csv file is saved in the new dataframe

# New in df by filename
df_new=df[(~df['File_name'].isin(old_data['File_name']))] # added files
old_old=old_data[(~old_data['File_name'].isin(df['File_name']))] #removed files

print('Removing: ', len(old_old),' Files')
print('Adding: ',len(df_new), 'Files')

df_0=old_data.append(df_new) #add new files
j=df_0.drop(old_old.index,axis=0)
j.sort_values(by=['Publisher','Group', 'second_group', 'Title','Year','Issue'],inplace=True)
j.reset_index()

# put old erased file notes somewhere else
dp=deprecated_file.append(old_old)
#dp.sort_values(by=['Publisher','General_Group', 'Title', 'Arc','second_group', 'Year','Issue'],inplace=True)
#dp.sort_values(by=['Publisher','Group', 'Title', 'Writer','second_group', 'Year','Issue'],inplace=True)
dp.sort_values(by=['Publisher','Group', 'second_group', 'Title','Year','Issue'],inplace=True)
dp.reset_index()

print('Done.\n')

#----------
# Stats
#----------

(size, files, percent)=stats(j)

#-----------
# End
#-----------
print('Collection in variable: j')

save_and_backup(j, 'comics_db.csv')
save_and_backup(dp, 'dep_comics_db.csv')
