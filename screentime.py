import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mt
import sys
# Screentime data from .csv

def load_screen(filename='~/Desktop/Comics/codes/cap.csv'):
	'''Load .csv of screentimes to pandas dataframe'''
	df=pd.read_csv(filename,index_col=0)
	return df

def to_times(df,skipcol=0,skiprow=0):
	'''Converts df values to timedelta objects'''
	return df.iloc[skiprow:,skipcol:].apply(pd.to_timedelta)

def load_csv(filename='~/Desktop/Comics/codes/cap.csv'):
	df1=load_screen()
	df=to_times(df1,skipcol=3,skiprow=2)
	return df1, df

def series(df1, subset=None, level=0):
	df2=df1.drop('Runtime')

	if subset==None: # this is for the whole MCU
		df=to_times(df2,skipcol=3,skiprow=2)
		c_run=df.sum(axis=1)
		c_series=c_run.sort_values(ascending=False)
		film_num=1
		max_time=None
	
	else: #select subset group	
		df2=df2.T.set_index('Group',append=True).T # sets Group row as an index
		p=df2.xs(subset,axis=1,level=1)
		film_num=len(p.columns)
		p=to_times(p,skiprow=1)
		max_time=pd.to_numeric(p.max())
		c_series=p[p.columns[level]].sort_values(ascending=False)
	return c_series, (film_num,max_time)

def series_all(df1, subset='Thor'):
	df2=df1.drop('Runtime')
	df2=df2.T.set_index('Group',append=True).T # sets Group row as an index
	p=df2.xs(subset,axis=1,level=1)
	film_num=len(p.columns)
	p=to_times(p,skiprow=1)
	max_time=pd.to_numeric(p.max())
	r=p.sum(axis=1)
	c_series=r.sort_values(ascending=False)

	return c_series

def trip_plot(df1, subset='Thor',num_chars=6,units='min',colors=None, fig_num=1):
	c_series,(film_num,max_time)=series(df1,subset=subset,level=0)
	
	runs=[]
	for a in range(0,film_num):
		b,c=series(df1,subset=subset,level=a)
		runs.append(b)
	
	runs=runs[::-1] # so chronologically

	if units=='hrs':
		un=3600.*1E9
	else:
		un=60.*1E9

	# Need this to determine consistent y-scale across plots
	max_time=max_time.max()/un
	max_time=(np.floor(max_time/10)+1)*10

	# plots
	fig=plt.figure(fig_num,figsize=(9,4))
	for a in range(0,film_num):
		s=plt.subplot(1,film_num,a+1)
				
		bars=runs[a].index[:num_chars]
		heights=pd.to_numeric(runs[a].values[:num_chars])/un #timedelta to minutes
		ypos=np.arange(len(bars))
		
		# get colors
		vill=df1['Colors'].to_dict()
		vills=[vill[x] for x in bars]		

		plt.title(runs[a].name)	
		plt.bar(ypos, heights,color=vills)
		plt.xticks(ypos, bars, rotation=45)
		#plt.ylim(ymax=max_time)
		plt.ylim(ymax=80) # same scale for everyone
		plt.ylabel('Screentime ('+units+')')
		
		s.spines['right'].set_visible(False)
		s.spines['top'].set_visible(False)
		# make axes invisible
		if a>0:
			s.yaxis.set_visible(False)
			s.spines['left'].set_visible(False)
	plt.subplots_adjust(bottom=0.2,wspace=0.1)
	#plt.show()

	return runs

def plot_screentimes(c_series,subset=None, movie=None, num_chars=6,colors=None, units='min'):
	'''Bar plot of Screentimes for characters.'''
	if units=='hrs':
		un=3600.*1E9
	else:
		un=60.*1E9
	plt.figure(figsize=(9,4))
	c=plt.subplot(1,1,1)
	bars=c_series.index[:num_chars]
	heights=pd.to_numeric(c_series.values[:num_chars])/un #timedelta to minutes
	ypos=np.arange(len(bars))

		
	vill=df1['Colors'].to_dict()
	vills=[vill[x] for x in bars]		
	plt.bar(ypos, heights,color=vills)
	plt.xticks(ypos, bars, rotation=45)
	plt.ylabel('Screentime ('+units+')')
	plt.subplots_adjust(bottom=0.3)
	c.spines['right'].set_visible(False)
	c.spines['top'].set_visible(False)	
	#plt.show()
	return None

def plot_percents(c_series,subset=None, movie=None, num_chars=6,colors=None, units='min'):
	'''Bar plot of Screentimes for characters in percentage of total screentime.'''
	plt.figure(figsize=(9,4))
	c=plt.subplot(1,1,1)
	c_series=c_series.sort_values(ascending=False)
	bars=c_series.index[:num_chars]
	heights=pd.to_numeric(c_series.values[:num_chars]) #timedelta to minutes
	ypos=np.arange(len(bars))
	vill=df1['Colors'].to_dict()
	vills=[vill[x] for x in bars]		
	plt.bar(ypos, heights,color=vills)
	plt.xticks(ypos, bars, rotation=45)
	plt.ylabel('Screentime Percentage (%)')
	#plt.ylim(ymax=60)
	plt.subplots_adjust(bottom=0.3)
	c.spines['right'].set_visible(False)
	c.spines['top'].set_visible(False)	
	#plt.show()
	return None
#--------------------
# Main Stuff
#------------------

df1, df=load_csv()

# Add colour column
color_dict={'V':'k','G':'0.5','Stark':'#b60000', 'Cap':'#002ea5', 'Avengers':'#3f829d', 'IM':'#b60000', 'CA':'#002ea5','Thor':'#0691f3', 'GotG':'#307b1c', 'Team':'b','AM':'cyan','Hulk':'g','Next':'magenta','Strange':'gold','Parker':'#980002','BP':'#380282','Marvel':'darkgreen','Ant':'cyan'}

d=df1[['Affiliation','Alignment']]
d=d[3:]
cs=[]
for a in d.values:
	if a[1]=='V':
		cs.append('k')
	elif a[1]=='G':
		cs.append('0.75')
	else:
		cs.append(color_dict[a[0]])

# Make a colour column
df1['Colors']=[None]*3+cs
cols=df1.columns.tolist()
cols=cols[:2]+[cols[-1]]+cols[2:-1]
df1=df1[cols]

# Total runtimes by group
runs=df1.loc[['Group','Runtime']].T
runs['Runtime']=runs['Runtime'].apply(pd.to_timedelta)
runs_tot=runs.groupby('Group').sum()
tots=runs_tot.to_dict()['Runtime']
#-------------
# Plots
#-------------

# by group
un_groups=df1.loc['Group'].unique()[2:]

for num, group in enumerate(un_groups):
	# lets make these percentages
	tot=tots[group]
	j=trip_plot(df1,subset=group,fig_num=num)
	#p=series_all(df1,subset=group)/tot*100
	#r=plot_percents(p)

# in total
c_series,x=series(df1)
c=plot_screentimes(c_series,num_chars=10,colors='k',units='hrs')

plt.show()
