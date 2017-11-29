from numpy import *
import pandas as pd
import plotly
import plotly.graph_objs as go
import datetime
import numpy as np
plotly.offline.init_notebook_mode()

'''This code is to do Artist and Writer top ten bars.'''

df=pd.read_csv('/Users/ksakamoto/Desktop/new_orange.csv')

# get writers list
rank=9
writers=df
writers=df.query('Story_Rank>=@rank')
writers.replace(to_replace={'Type':{0:1,2:1,3:1,4:1}},inplace=True)
k=where(writers.Type==5)[0]
writers.reset_index(inplace=True)
writers.Type.ix[k]=writers.Issue_end[k]-writers.Issue[k]+1
writers.Artist=writers.groupby('Writer')['Type'].transform('sum')
writers.Issue=writers.groupby(['Writer','Title'])['Type'].transform('sum')
w=writers[['Artist','Writer','Title','Issue']]
w.sort_values(by=['Artist','Writer','Issue'],ascending=False,inplace=True)
w.drop_duplicates(inplace=True)
writers=list(w['Writer'].drop_duplicates())
w1=[]
for a in writers:
	w1.append(a.capitalize())
bulk=list(w.drop_duplicates(subset=['Writer'])['Artist'])
trace=go.Bar(x=w1[:2],y=[bulk[:2],bulk[:2]])
#trace1=go.Bar(x=w1[:10],y=array(bulk[:10])-2)
#lay=go.Layout(xaxis=dict(zeroline=False, title='#Pages'),yaxis=dict(title='Score'),legend=dict(x=0.2,y=0.4))
fig=go.Figure(data=[trace])
plotly.offline.plot(fig)
