import numpy as np
import pandas as pd
import re
import codecs
import datetime as dt
import os, sys

'''Take the final dialogue file and does stuff to it.'''

# Load files
foldername='/Users/ksakamoto/Desktop/Comics/codes/words_sub/'

prefix='bp'
filename='/Users/ksakamoto/Desktop/Comics/codes/words_sub/'+prefix+'_sub.csv'
csv=pd.read_csv(filename)
csv.drop(labels='Unnamed: 0',axis=1, inplace=True)

cap='/Users/ksakamoto/Desktop/Comics/codes/cap.csv'
cl=pd.read_csv(cap)
caps=cl.copy(deep=True)
caps.set_index('Title',inplace=True) #actual character names
caps.iloc[3:,2:]=0

# Gt time data
cl.set_index('Title',inplace=True)
times=cl.iloc[2:,2:].apply(pd.to_timedelta)

# Old Data

df1=pd.read_csv('/Users/ksakamoto/Desktop/Comics/codes/cap.csv',index_col='Title')
cols=df1.columns[2:]
c_fun=['av4','cm','ant2','av3','bp','thor3','sm','gotg2','strange','cap3','ant1','av2','gotg1','cap2','thor2','iron3','av1','cap1','thor1','iron2','hulk','iron1']
j=list(zip(c_fun,cols))
j=dict(j)

dic={'Hulk':'Bruce', 'Ancient one':'Ancient One', 'Red skull':'Red Skull', 'The collector':'The Collector','Hawkeye':'Clint','Pym':'Hank','Stan lee':'Stan Lee', 'Yon-rogg':'Yon-Rogg', 'Minn-erva':'Minn-Erva','Att-lass':'Att-Lass','Supreme intelligence': 'Supreme Intelligence','Bron-char':'Bron-Char', 'The collector': 'The Collector'}
# Clean entries

def word_process(string):
	string=string.lstrip()
	string=string.rstrip()
	string=string+' '
	
	string=re.sub('\n','',string)
	string=re.sub('<i>','',string)
	string=re.sub('</i>','',string)
	string=re.sub("\.\.\.",',',string)
	string= re.sub('-','- ',string)
	return string

def get_words(string):
	s=string.split(' ')
	s_list=list(filter(None,s))
	return len(s_list)

def word_count(df):
	i=df.groupby('Character')['words'].sum()
	return i.sort_values(ascending=False)

def line_count(df):
	h=df['Character'].value_counts()
	return h

# Go through the folder
sore=[]
titles=[]
for root, dirs, files in os.walk(top=foldername):
	for file in files:
		try:
			file_true=file.split('.')[0]
			file_true=file_true.split('_')[0]
			csv=pd.read_csv(root+'/'+file)
			csv.drop(labels='Unnamed: 0',axis=1, inplace=True)
			lines=csv['line']
			stripped_lines=lines.apply(lambda x : word_process(x))
			count_words=stripped_lines.apply(lambda x : get_words(x))
			csv['line']=stripped_lines
			csv['words']=count_words
			titles.append(j[file_true])
			sore.append((j[file_true],csv))
		except ParserError:
			pass

alls=pd.DataFrame(data=sore,columns=['Movie','series'])
		
apps=[]
# Amalgamate into 'Lines'
for series in alls['series'][:]:
	starts=[]
	ends=[]
	df=series.copy(deep=True)
	df['start']=df['start'].apply(pd.to_datetime)
	df['end']=df['end'].apply(pd.to_datetime)
	starts.append(df['start'][0])

	char_line=[df['Character'].iloc[0]]
	text=[df['line'].iloc[0]]
	complete_line=[]
	for i in range(1,len(df)):
		line=df['line'].iloc[i]
		start=df['start'].iloc[i] # this entry's start time
		end=df['end'].iloc[i-1] # last entry's end time
		end_new=df['end'].iloc[i]
		char=df['Character'].iloc[i]
		if char== char_line[-1]: # if same character is speaking
			if (end+dt.timedelta(seconds=2))>=start:
				text.append(line)
				#print(text)
			else:
				text_new=' '.join(text)
				text=[]	
				#print('---'+text_new)
				complete_line.append(text_new)
				char_line.append(char)
				text.append(line)
				starts.append(start)
				ends.append(end)
				#print(text)

		elif char!=char_line[-1]: # different character speaking
			text_new=' '.join(text)
			text=[]
			complete_line.append(text_new)
			#print(text_new)
			char_line.append(char)
			text.append(line)
			starts.append(start)
			ends.append(end)

		# accomodate for the last iteration
		if i==(len(df)-1) and char!=char[-1]:
			char_line.append(char)
			text_new=' '.join(text)
			complete_line.append(text_new)
			ends.append(df['end'].iloc[-1])		
			#print(text_new)
			
	data=list(zip(starts, ends, char_line,complete_line))
	df1=pd.DataFrame(data=data,columns=['start','end','Character','line'])
	df1['words']=df1['line'].apply(lambda x : get_words(x))
	
	# Check that we haven't lost words

	if df1['words'].sum()!=df['words'].sum():
		print('Bad job, return to count school at line 49.')

	apps.append(df1)

#sys.exit(0)

for i, series in enumerate(apps):
	#r=series.groupby('Character')['line'].sum()
	r=word_count(series)
	#r=line_count(series)
	title=alls['Movie'][i]
	#series.to_csv(title+'_line.csv')
	for ind, name in enumerate(r.index):
		nop=name.lower()
		nop=nop[0].upper()+nop[1:]
		try:
			nop=dic[nop]
		except KeyError:
			pass
		if any(caps.index==nop)==True:
			caps.loc[nop,title]+=r[ind]
		else:
			pass
			#print(name)

caps.to_csv('text_word.csv')

# Stats from subs
slice=caps.iloc[3:,2:]
place=slice.sum()
c=list(zip(place.index,place.values))
c=pd.DataFrame(data=c,columns=['Movie','partial'])
c.sort_values(by='Movie',inplace=True)
p=c[c.partial!=0.]

s=[]
for i in apps:
	s.append(i['words'].sum())
d=list(zip(titles,s))
d=pd.DataFrame(data=d,columns=['Movie','sum'])
d.sort_values(by='Movie',inplace=True)

p['sum']=d['sum'].values

# by character
n=slice.T.sum()
n.sort_values(ascending=False,inplace=True)

data=list(zip(alls['Movie'],apps))
new_data=pd.DataFrame(data=data,columns=['Movie','lines'])
#new_data.to_csv('lines_series.csv')


