from numpy import *
import pandas as pd
import plotly
import plotly.graph_objs as go 
import datetime
import numpy as np
plotly.offline.init_notebook_mode()

# df.drop('column_name', axis=1, inplace=True)
# df[(df.A == 1) & (df.D == 6)]

#-----Colour schemes---------------#
petrichor=['#b1ecbb','#06a8ac', '#014e70','#f46e15','#ffbf00']
emergency=['#dfbbbb','#789a63','#6c5d85','#645178','#855873']
edge=['#222222','#71e6b5','#09b4f6','#32526e','#3c3b3b']
drsrpt=['#0e3d51','#85cebb','#ef3e32','#f99e1c','#8c9697']
drs1=['#0C3141','#0D3749','#0E3D51','#265062','#3E6373','#567684','#6E8995','#869CA6','#9EAFB7','#B6C2C8','#CED5D9']+['#E6E8EA']*10+['#FFFFFF']*10
#drs1=['#0E3D51','#265062','#3E6373','#567684','#6E8995','#869CA6','#9EAFB7','#B6C2C8','#CED5D9','#E6E8EA']+['#FFFFFF']*10
drs2=['#85CEBB','#91D3C2','#9DD8C9','#A9DDD0','#B5E2D7','#C1E7DE','#CDECE5','#D9F1EC','#E5F6F3']+['#F1FBFA']*10
drs3=['#EF3E32','#F15147','#F3645C','#F57771','#F78A86','#F99D9B','#FBB0B0','#FDC3C5','#FFD6DA']+['#FFE9EF']*10
missemilys=['#105378','#90c9e8','#ff7302','#ffa902','#f6f6f6']
nondescript=['#fdff3c','#c9a244','#ae715d','#5d9252','#606c85']
tvny=['#ffffff','#ffba9c','#e7ff8f','#12aea2','#3769d2']
fond=['#222222','#554455','#eeeedd','#cc9999','#996677']
disseminada=['#2d2d2d','#374165','#eeeeee','#ad6284','#5f436f']
amrido=['#000000','#008080','#ffffff','#dddddd','#bbbbbb']
wolfoc=['#ffffff','#e5cb99','#ffef8f','#77b7c9','#2b2b2b']
sugarbaby=['#443333','#aa9999','#eeddcc','#ddbbaa','#aa7766']
cappuccino=['#4b3832','#854442','#fff4e6','#3c2f2f','#be9b7b']
shinyphan=['#000000','#0f2637','#5d4d48','#cce1e6','#e9e0c9']
frank=['#3f0e1a','#483336','#777e90','#384b75','#f0e7df']
cedar=['#bb1515','#e0cda7','#2a334f','#6b4423','#ac8f57']
stei=['#a88215','#110f34','#204832','#7b4615','#62756b']
stei3=['#0a2036','#ae7120','#93ae6f','#6c6565','#02362c']
arlequins=['#135c0e','#d9b500','#136a8a','#b30202','#570033']
icecream=['#6b3e26','#ffc5d9','#c2f2d0','#fdf5c9','#ffcb85']
crayola=['#ed0a3f','#e77200','#fed85d','#01786f','#2d383a']
community=['#931031','#f06d3d','#ffac00','#354458','#78c0a8']
gsheet=['#ec3a3a','#e56f46','#dd9f40','#e7d87d','#82c3ff']
bootstrap=['#d9534f','#f9f9f9','#5bc0de','#5cb85c','#428bca']
zukyny=['#474c49','#52946b','#ee9851','#eac761','#f1e6d0']
zukyny_mod=['#52946b','#ee9851','#474c49','#eac761','#f1e6d0']
zukyny2=['#52946b','#74AA89','#ee9851','#F2AC73','#474c49','#6B706D','#eac761','#f1e6d0']
blacks=['#474C49','#595E5B','#6B706D','#7D827F','#8F9491','#A1A6A3','#B3B8B5','#C5CAC7','#D7DCD9','#E9EEEB']+['#FFFFFF']*10
bs=[]
os=['#EE9851','#F0A262','#F2AC73','#F4B684','#F6C095','#F8CAA6','#FAD4B7','#FCDEC8','#FEE8D9','#FFF2EA']+['#FFFFFF']*10
gs=['#427655','#4A8560','#52946B','#639F7A','#74AA89','#85B598','#96C0A7','#A7CBB6','#B8D6C5','#C9E1D4','#DAECE3','#EBF7F2']+['#FFFFFF']*10
venus=['#632416','#cc3a00','#ff9e43','#ffdc79','#ffebad']
flamingo=['#fdd5d8','#fe9f9a','#e46967','#933642','#5e3f43']

#-----Define html color schemes----#
blues=['CadetBlue','SteelBlue','LightSteelBlue','LightBlue','LightSkyBlue','SkyBlue','CornflowerBlue']#,'DodgerBlue','RoyalBlue'] #10
yellows=['Gold','Yellow','LightYellow','LemonChiffon','Moccasin','PaleGoldenRod','Khaki'] #7
cyans=['DarkTurquoise','MediumTurquoise','Turquoise','Aquamarine','PaleTurquoise','LightCyan','Cyan','Aqua'] #8
greens=['DarkGreen','Green','ForestGreen','SeaGreen','MediumSeaGreen','MediumAquaMarine','SpringGreen','LightGreen','PaleGreen'] #9
oranges=['OrangeRed','Tomato','Coral','DarkOrange','Orange'] #5
reds=['FireBrick','Crimson','Red','IndianRed','LightCoral','DarkSalmon','Salmon','LightSalmon'] #8
pinks=['Pink','LightPink','HotPink','PaleVioletRed','MediumVioletRed'] #
indigos=['RebeccaPurple','DarkSlateBlue','SlateBlue','MediumSlateBlue','MediumPurple'] #5
purples=['Purple','DarkMagenta','BlueViolet','DarkViolet','DarkOrchid','MediumOrchid'] #6
violets=['Violet','Orchid','Plum','Thistle','Lavender'] #5
greys=['DimGray','Gray','DarkGray','Silver','LightGray','Gainsboro','white'] #7
browns=['SaddleBrown','Sienna','DarkGoldenRod','Peru','Burlywood','Tan','Wheat','BlanchedAlmond']#8
col=[blues+blues+blues+blues,greens+yellows[2:]+greens,indigos+purples+indigos+purples,cyans+cyans,reds+oranges,yellows+yellows+yellows,browns,greys,pinks]
#col=[drs1+drs1,drs2+drs2,drs3+drs3,cyans+cyans,reds+oranges,yellows+yellows+yellows,browns,greys,pinks]
rain=[blues[0],greens[0],indigos[0],cyans[0],reds[0],yellows[0],browns[0],greys[0]]

def scatter(df):
	cond=1
	df1=df.query('Read==@cond')
	years=array(df1['Year'])
	#month=df1['Month 1']
	time=[]
	for a in range(0,len(years)):
		#time.append(datetime.datetime(years[a],month[a],1))
		k=np.random.random_integers(1,12)
		#print a
		time.append(datetime.datetime(int(years[a]),k,1))
	ranks=df1['Story_Rank']
	trace=go.Scatter(x=time,y=ranks,mode='markers',text=list(df1['Title']))
	lay=go.Layout(xaxis=dict(zeroline=False, title='#Pages'),yaxis=dict(title='Score'),legend=dict(x=0.2,y=0.4))
	fig=go.Figure(data=[trace],layout=lay)
	plotly.offline.plot(fig)
	return None	

def form(trace,percent):
	c=array([round(x,2) for x in trace['values']/sum(trace['values'])*100.])
	c=c[where(c>percent)[0]]
	c=list(map(str,c))
	r=trace['labels']
	for a in range(0,len(c)):
		c[a]=r[a]+'\n'+c[a]+'%'
	counts=len(r)-len(c)
	c=c+[None]*counts
	trace['text']=c
	return None

def plot_all(df):
	'''Plots Publisher and read/unread pie charts'''
	#Publisher
	p=df[['Publisher','Artist','Size']]
	p['Artist']=df.groupby('Publisher')['Size'].transform('sum')
	c=p[['Publisher','Artist']].drop_duplicates()
	c.sort_values(by='Artist', ascending=False,inplace=True)	
	
	values=list(c['Artist']/1000.)
	labels=list(c['Publisher'])
	# make 'other category'
	c=where(values/sum(values)*100<1)[0]
	values=values[:c[0]]+[array(values)[list(c)].sum()]
	labels=labels[:c[0]]+['Other']	

	textfont={'size':18,'color':'black'}
	domain={'x':[0.0,0.4]}#,'y':[0.5,1.1]}
	mark1=dict(colors=zukyny_mod)

	# Read/Unread by Publisher
	p=df[['Read','Publisher','Size','Writer','Artist']]
	p.fillna(0,inplace=True)
	p['Artist']=p.groupby(['Read','Publisher'])['Size'].transform('sum')
	p['Writer']=p.groupby(['Publisher'])['Size'].transform('sum')
	p.drop(axis='columns',labels='Size',inplace=True)
	c=p.drop_duplicates()
	k=c.sort_values(by=['Writer','Read'],ascending=False)	
	d=k.groupby('Read')['Artist'].transform('sum')
	d.drop_duplicates(inplace=True)
	values2=list(k['Artist']/1000.)
	cols=['SteelBlue','LightSteelBlue','FireBrick','IndianRed','Green','SeaGreen','RebeccaPurple','LightYellow','Gray']
	mark2=dict(colors=zukyny2)
	l=array(k['Publisher'])
	l=l+', '
	pl=[]
	for a in k.Read:
		if a==1.0:
			pl.append('Read')
		else:
			pl.append('Unread')
	l=l+pl
	labels3=l
	
	#labels3=['Marvel, Read','Marvel,\nUnread','DC, Read','DC, Unread','Image, Read','Image, Unread','BOOM, Read','Vertigo, Unread']
	domain2={'x':[0.6,1.0]}#,'y':[0.5,1.1]}	
	textfont2=dict(size=15,color='black')

	trace=go.Pie(sort=False, hoverinfo='label+percent+value',textinfo='text', domain=domain,labels=labels,textfont=textfont,marker=mark1,values=values,text=[None]*len(labels),showlegend=False,hole=0.35)
	trace2=go.Pie(sort=False, marker=mark2, hoverinfo='label+percent+value',textinfo='text', labels=labels3,rotation=38, domain=domain2, text=[None]*len(labels3),textfont=textfont2,values=values2,hole=0.35,showlegend=False)
	
	#label stuff, ignore slices less than 5%
	form(trace,5)
	form(trace2,5)
	data=[trace,trace2]

	# layout stuff
	d=list(d/1000.)
	total_size=round(sum(trace['values']),1)
	total_size_str=str(total_size)+' GB'
	read=round(d[0],1)
	read=str(read)+' GB'
	unread=round(d[1],1)
	unread=str(unread)+' GB'	

	sub1=dict(font=dict(size=18),text='By Publisher',x=0.15,y=1.02,showarrow=False)
	sub2=dict(font=dict(size=18),text='Read by Publisher',x=0.88,y=1.02,showarrow=False)
	t_size=dict(font=dict(size=20),text='Total Size:\n'+total_size_str,x=0.15,y=0.505,showarrow=False)
	r_size=dict(font=dict(size=16),text='Read: '+read+'\nUnread: '+unread,x=0.865,y=0.505,showarrow=False)

	lay=go.Layout(title='Comic Collection',titlefont=dict(size=25,color='black'),annotations=[sub1,sub2,t_size,r_size])

	fig=go.Figure(data=[trace,trace2],layout=lay)
	plotly.offline.plot(fig)
	return values,labels#trace,trace2

def plot_groups(df):
	'''By General_Group and Story Rank'''
	# General Group
	#rs=['#ab2121','#b22222', '#d62929', '#da3e3e', '#de5454','#e26969', '#e77e7e', '#eb9494','#efa9a9','#f3bfbf','#f7d4d4','#fbeaea']+['#ffffff']*8 #11
	d={'Marvel':gs,'DC':os,'Image':blacks,'Other':[petrichor[1]],'Legendary':[zukyny[0]],'Valiant':[zukyny[2]],'Wildstorm':[zukyny[1]],'BOOM':[zukyny[3]],'Vertigo':[zukyny[4]],'Dark Horse':greys,'Soleil':[venus[0]],'Mpress':[venus[1]], 'Avatar':[venus[2]], 'Europe':[venus[3]]}
	p=df[['Group','General_Group','Artist','Size','Publisher','Writer']]
	p['Artist']=df.groupby('General_Group')['Size'].transform('sum')
	p['Writer']=p.groupby('Publisher')['Size'].transform('sum')
	c=p[['General_Group','Group','Artist','Publisher','Writer']].drop_duplicates()
	c1=p[['General_Group','Artist','Publisher','Writer']].drop_duplicates()
	other=c1.sort_values(by=['Writer','Artist'],ascending=False)
	other2=c.sort_values(by=['Writer','Artist'],ascending=False)
	other2.drop_duplicates(subset='General_Group',inplace=True)
	labs=other2['General_Group']+'\n'+other2['Group']
	labs=list(labs)
	col=[]
	names=[]
	for a in other['Publisher'].drop_duplicates():
		cnew=len(other[(other.Publisher==a)])
		col=col+d[a][:cnew]
		names.append(a)	

	values=list(other['Artist']/1000.)
	labels=list(other['General_Group'])
	textfont={'size':15,'color':'black'}
	domain={'x':[0,0.4]}#, 'y':[0.5,1]}
	
	# ranked
	textfont2={'size':16,'color':'black'}
	domain2={'x':[0.6,1]}#,'y':[0.5,1]}	

	p=df[['Story_Rank','Size','Artist','Read']]
	p.fillna(0,inplace=True)
	p['Artist']=p.groupby(['Read','Story_Rank'])['Size'].transform('sum')
	c=p[['Story_Rank','Artist','Read']].drop_duplicates()
	c.sort_values(by=['Read','Story_Rank'],ascending=False,inplace=True)
	labels2=['10.0','9.0','8.0','7.0','6.0','Unranked','Unread']
	text2=[None,'9.0','8.0','7.0','6.0','Unranked','Unread']
	values2=c['Artist']
	c=flamingo[::-1]+['DimGrey','Gainsboro']
	c=['#374165','#4B5474','#5F6783','#737A92','#878DA1']+['DimGrey','Gainsboro']
	mark2={'colors':c}

	names=['General Group']
	#read/unread
	p=df[['Size','Read','Artist']]
	p.fillna(0,inplace=True)
	p['Artist']=p.groupby(['Read'])['Size'].transform('sum')
	c=p[['Artist','Read']].sort_values(by='Read',ascending=False)
	c.drop_duplicates(inplace=True)
	vs=c['Artist']
	ls=['Read','Unread']
	
	trace3=go.Pie(sort=False,marker=dict(colors=['DimGray','White']),labels=ls,hoverinfo='label+percent',domain=dict(x=[0.12,0.28],y=[0.42,0.58]),values=vs,textinfo='none',showlegend=False)
	trace2=go.Pie(sort=False,rotation=83,marker=mark2,hoverinfo='label+percent', domain=domain2,labels=labels2,textfont=textfont2,values=values2,textinfo='text',text=text2,showlegend=False,pull=True)
	trace=go.Pie(marker=dict(colors=col),textinfo='none',text=list(other2['Group']),name=names,sort=False, domain=domain,labels=labels,hoverinfo='label+text+percent+name',textfont=textfont,values=values,rotation=140,hole=0.25,showlegend=False)
	#form(trace,5)

	lay=go.Layout(title='Comic Collection',titlefont=dict(size=25),annotations=[dict(font=dict(size=18),text='By Subject',x=0.15,y=1.02,showarrow=False),dict(font=dict(size=18),showarrow=False,x=0.85,y=1.02,text='Story Rank')])
	fig=go.Figure(data=[trace,trace2,trace3],layout=lay)
	plotly.offline.plot(fig)
	return trace

def plot_other(df,pub=None):
	'''Breakdown by top eight groups by title'''
	c=df[['Title','Type','Publisher','second_group','General_Group','Group', 'Artist','Size']]
	d=c.copy()
	if pub==None:
		pass
	else:
		d=d[d.Publisher==pub]
	d['Artist']=d.groupby(['General_Group'])['Size'].transform('sum')
	d.drop_duplicates(subset='Artist',inplace=True)
	d.sort_values(by='Artist',ascending=False,inplace=True)

	t=[]
	# With sub divisions
	twodiv=list(d.General_Group)[:8]
	names=list(d.Group)[:8]
	anns=[]
	for count in range(0,len(twodiv)):
		gengroup=twodiv[count]
		c=df[['Title','Type','second_group','General_Group','Group', 'Artist','Size']]
		r=c[(c.General_Group==gengroup)]
		r.fillna(0,inplace=True)	
		
		if gengroup!='Ultimate Universe':
			r.ix[r.Type==4,'second_group']='Minis'
			r.ix[r.Type==2, 'second_group']='Specials'
			if gengroup!='Events':
				r.ix[r.second_group==0,'second_group']='Series'
		r['Artist']=r.groupby(['General_Group','second_group'])['Size'].transform('sum')
		r['Type']=r.groupby(['General_Group','Title'])['Size'].transform('sum')
		r.drop(axis='columns',labels=['Size'],inplace=True)
		r.drop_duplicates(inplace=True)
		r.sort_values(by=['Artist','Type'],ascending=False,inplace=True)
		r['Artist']=r.groupby('second_group').transform('count')
		cnew=array(r['second_group'])
		k=r[['Artist','second_group','General_Group']].drop_duplicates()
		l=array(k['Artist'])
		l=list(map(int,l))
		cols=[]
		for i in range(0,len(l)):
			try:
				cols=cols+col[i][:l[i]]
			except IndexError:
				cnew=l[i]-len(col[i])
				li=col[i]+['white']*cnew
				cols=cols+li
		labels=r['Title']
		values=r['Type']
		textfont={'size':13,'color':'black'}
	
		# domains

		spanx=(0,1.0)
		spany=(0,1.0)

		xdiv=linspace(spanx[0],spanx[1],5)
		ydiv=linspace(spany[0],spany[1],3)
		if count<4:
			y1=[ydiv[1],ydiv[2]]
			count1=count
		if count>3:
			y1=[ydiv[0],ydiv[1]]
			count1=count-4

		xmed=mean([xdiv[count1],xdiv[count1+1]])
		if count==7:
			xmed+=0.04
		elif count==3:
			xmed+=0.03
		elif count==0 or count==4:
			xmed-=0.06
		ymed=y1[0]
		if count==0:
			ymed-=0.04
		ann=dict(font=dict(size=15),showarrow=False,text=gengroup,x=xmed,y=ymed)
		domain=dict(x=[xdiv[count1],xdiv[count1+1]],y=y1)
		mark={'colors':cols}
		trace=go.Pie(hoverinfo='name+text+label+percent',scalegroup='others',hole=0.3, sort=False, domain=domain, name=names[count], textfont=textfont, marker=mark,labels=labels, values=values, text=cnew, textinfo='none',showlegend=False)	
		
		# read circles
		sides=0.10
		domain=dict(x=[xdiv[count1]+sides,xdiv[count1+1]-sides],y=[y1[0]+sides,y1[1]-sides])
		d=df[['General_Group','Read','Story_Rank','Size','Writer']]
		d=d[(d.General_Group==gengroup)]
		d.fillna(0,inplace=True)
		unread=d[(d.Read==0.0)]['Size'].sum()
		d=d[(d.Read==1.0)]
		read=d['Size'].sum()
		labels=['Read','Unread']
		mark={'colors':['DimGray','White']}
		text=['Read',None]
		values=[read,unread]
		tnew=go.Pie(direction='counterclockwise',text=text,values=values, marker=mark,hoverinfo='label+percent',scalegroup='read',sort=False,domain=domain,labels=labels,textinfo='none',showlegend=False)	
		t.append(trace)
		t.append(tnew)
		anns.append(ann)
	
	lay=go.Layout(title='Comic Collection: Top Eight Groups',titlefont=dict(size=20),annotations=anns)
	fig=go.Figure(data=t,layout=lay)
	plotly.offline.plot(fig)
	return t
