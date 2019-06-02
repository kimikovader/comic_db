import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as pt
#import kim_help

'''Play file for word count stuff'''

def get_words(string):
	try:
		s=string.split(' ')
		s_list=list(filter(None,s))
		l=len(s_list)
	except AttributeError:
		l=np.nan
	return l

# Start file
root='/Users/ksakamoto/Desktop/Comics/codes/'
filename1='text_word.csv'
filename2='lines_series.csv'
df1=pd.read_csv(filename2)#,index_col=0)
df=pd.read_csv(filename1,index_col=0)

d=df.iloc[3:,2:]
p=d['Age of Ultron'].apply(lambda x : get_words(x))
p.sort_values(ascending=False, inplace=True)
