import plotly
from plotly.tools import FigureFactory as FF
import pandas as pd
import plotly.graph_objs as go
import datetime
import matplotlib

def make_strings(df):
	groups=['Ironman']
	all_starts=[]
	all_ends=[]
	all_tasks=[]
	for a in groups:
		d=df[(df.Group==a)]
		print d
		d=d[(d.Type!=1) & (d.Type!=2)]
		d=d[['Type','Writer','Title','Month 1','Month 2','Year']]
		d.dropna(subset=['Month 1'],inplace=True)

		# for collected editions
		r=d[(d.Type==5)]
		r1=r.drop_duplicates(subset=['Writer','Title'])
		st=r1['Month 1'].astype('int')
		st=st.astype('str')
		r2=r.drop_duplicates(subset=['Writer','Title'],keep='last')
		en=r2['Month 2'].astype('int')
		en=en.astype('str')
	
		y=r1['Year'].astype('str')
		y1=r2['Year'].astype('str')
		starts_col=y+'-'+st
		ends_col=y1+'-'+en
		Tasks_col=r1['Title']
		#print starts_col, ends_col	
		# for minis
		c=d[(d.Type==4)]
			
		k=c.groupby(['Writer','Title']).head(1)
		k1=c.groupby(['Writer','Title']).tail(1)
		
		c=k['Month 1'].astype('int')
		c1=k1['Month 1'].astype('int')
		c1=c1.astype('str')
		c=c.astype('str')
		#print c1,c	
		y=k['Year'].astype('str')
		y1=k1['Year'].astype('str')
		
		starts_min=y+'-'+c
		ends_min=y1+'-'+c1
		Tasks_min=['Minis']*len(y)
		
		# reg series
		c=d[(d.Type==0)]
		k=c.groupby(['Title','Writer'])
	
		titles=[]
		writers=[]
		all_times=[]
		for a in k:
			writers.append(a[0][1])
			titles.append(a[0][0])
			m=map(int,list(a[1]['Month 1']))
			y=list(a[1]['Year'])
			time_temp=[]
			for i in range(len(m)):
				time_temp.append(datetime.datetime(y[i],m[i],1))
			breaks=[]
			for it in range(1,len(time_temp)):
				if time_temp[it]-time_temp[it-1]>datetime.timedelta(180): # break in days
					breaks.append(it)
			if len(breaks)>0:
				for ai in breaks:
					m1=time_temp[:ai]
					m2=time_temp[ai:]
					all_times.append(m1)
					all_times.append(m2)
					writers.append(a[0][1])
					titles.append(a[0][0])
			else:
				all_times.append(time_temp)		
		Tasks=titles
		starts=[]
		ends=[]	
		for ip in all_times:
			starts.append(str(ip[0]))
			ends.append(str(ip[-1]))
		task_names=writers
					
		all_tasks=Tasks+list(Tasks_col)+list(Tasks_min)
		all_starts=starts+list(starts_col)+list(starts_min)
		all_ends=ends+list(ends_col)+list(ends_min)
		all_names=task_names+[None]*len(list(ends_col))+[None]*len(list(ends_min))	
		data=[]
		for a in range(0,len(all_starts)):
			data.append(dict(Task=all_tasks[a],Start=all_starts[a],Resource=all_tasks[a],Finish=all_ends[a]))
		
		# make the same colors
		n=['Crimson','FireBrick','IndianRed','LightCoral','DarkSalmon','Salmon','LightSalmon','OrangeRed','Tomato']
		c=[]
		for a in n:
			knew=matplotlib.colors.colorConverter.to_rgb(a)
			k='rgb'+str(knew)
			c.append(k)
		semi=list(pd.Series(all_tasks).drop_duplicates())
		print semi
		cols={}
		for k,v in enumerate(semi):
			cols[semi[k]]=c[k]
	
		cls=[]
		for a in all_tasks:
			cls.append(cols[a])	
		fig=FF.create_gantt(data,colors=cls,width=1100,title=groups[0],opacity=0.75)
		
		# put a goddamn margin in
		m=dict(l=200)
		fig['layout']['margin']=m
			
		plotly.offline.plot(fig)
	return fig #titles, writers #,all_times,titles
