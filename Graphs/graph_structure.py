from numpy import *
import pandas as pd
import os, sys

def weights(series):
	n=pd.value_counts(series)
	return list(n)

def nodes_write(df):
	a=['Writer','Artist']
	weights=[]
	tiers=[]
	l=[]
	count=2
	for i in a:
		count-=1
		d=df[[i,'Size','Publisher']]
		d['Publisher']=d.groupby(i)['Size'].transform('sum')
		r=d[[i,'Publisher']].drop_duplicates()
		l=l+list(r[i])
		tiers=tiers+[count]*len(r)
		weights=weights+list(r['Publisher'])

	tiers=map(int,tiers)
	n=list(map(str,arange(0,len(l))))
	d={'id':n,'label':l, 'weights':weights, 'tiers':tiers}
	p=pd.DataFrame(data=d)
	p.where(p['weights']>80,inplace=True)
	p.drop_duplicates(subset='label',inplace=True)
	p.dropna(inplace=True)
	#p.reset_index(drop=True,inplace=True)
	l=list(p['label'])
	n=list(p['id'])
	new=dict(zip(l,n))
	#p.to_csv('nodes_write.csv', index=None)
	return p,new#,new2

def clean(node_data, edge_data):
	#filter for artist/writers
	k1=array(edge_data['source'])
	k2=array(edge_data['target'])
	f=where(k1==k2)[0]
	j=map(int,k1[f])
	node_data.set_value(index=j,col='tiers',value=3)
	node_data.to_csv('nodes_write.csv',index=None)
	return None

def nodes_group(df):
	a=df[['Writer','Size','Artist']]
	a['Artist']=a.groupby(['Writer'])['Size'].transform('sum')
	a.drop(axis='columns',labels='Size',inplace=True)
	gg=list(a['Writer'].drop_duplicates())
	size=list(a['Artist'].drop_duplicates())
	a=df[['General_Group','Size','Artist']]
	a['Artist']=a.groupby(['General_Group'])['Size'].transform('sum')
	a.drop(axis='columns',labels='Size',inplace=True)
	gg1=list(a['General_Group'].drop_duplicates())
	size1=list(a['Artist'].drop_duplicates())
	names=gg+gg1
	tiers=[0]*len(gg)+[1]*len(gg1)
	size=size+size1
	n=map(str, arange(0,len(names)))
	d={'id':n,'label':names, 'size':size, 'tiers':tiers}#, 'c_w':colors}
	p=pd.DataFrame(data=d)
	p.drop(where(array(p['size'])<5)[0],inplace=True)
	new=dict(zip(names,n))
	p.to_csv('nodes_groups.csv', index=None)
	return p, new# size, l #p,new,tiers
	
def nodes_pub(df):
	a=df[['Publisher','Writer','Artist']]
	a.replace(to_replace={'Publisher': {'Vertigo': None, 'BOOM': None, 'Dark Horse':None, 'Image':None}}, inplace=True)
	a.dropna(inplace=True)
	c=['size','writers_all','writers_all','art_all','art_pub']
	for i in c:
		a[i]=None
	# Size by complete number
	a['size']=a.groupby(['Publisher']).transform('count')
	a['writers_all']=a.groupby(['Writer']).transform('count')
	#a['writers_pub']=a.groupby(['Writer'])['Publisher'].transform('count')
	a['art_all']=a.groupby(['Artist']).transform('count')
	#a['art_pub']=a.groupby(['Artist'])['Publisher'].transform('count')
	a.drop_duplicates(inplace=True)
	
	size=[]
	names=[]
	weights=[]
	# add the all columns
	news=a[['Publisher','size']].drop_duplicates()
	names=names+list(news['Publisher'])
	size=size+list(news['size'])
	
	news1=a[['Writer','writers_all']].drop_duplicates()
	names=names+list(news1['Writer'])
	size=size+list(news1['writers_all'])
	
	news2=a[['Artist','art_all']].drop_duplicates()
	names=names+list(news2['Artist'])
	size=size+list(news2['art_all'])

	weights=[1,-1]
	for name in news1['Writer']:
		item='DC'
		it='Marvel'
		c=df.query('Writer==@name and Publisher==@item')['Writer']
		c=pd.value_counts(c)
		if len(c)<1:
			c=0
		else:
			c=c[0]
		c1=df.query('Writer==@name and Publisher==@it')['Writer']
		c1=pd.value_counts(c1)
		if len(c1)<1:
			c1=0
		else:
			c1=c1[0]
		total=c1*(-1)+c
		weights.append(total)		
	for name in news2['Artist']:
		item='DC'
		it='Marvel'
		c=df.query('Artist==@name and Publisher==@item')['Artist']
		c=pd.value_counts(c)
		if len(c)<1:
			c=0
		else:
			c=c[0]
		c1=df.query('Artist==@name and Publisher==@it')['Artist']
		c1=pd.value_counts(c1)
		if len(c1)<1:
			c1=0
		else:
			c1=c1[0]
		total=c1*(-1)+c
		weights.append(total)		

	n=map(str, arange(0,len(weights)))
	d={'id':n,'label':names, 'size':size, 'weights':weights}#, 'c_w':colors}
	p=pd.DataFrame(data=d)
	p['weights']=p['weights']/p['size']
	p['weights'].ix[0]=1.0
	p['weights'].ix[1]=-1.0
	p.drop(where(array(p['size'])<5)[0],inplace=True)
	new=dict(zip(names,n))
	p.to_csv('nodes_pub.csv', index=None)
	return p, new# size, l #p,new,tiers

def nodes(df):
	a=df[['Publisher','Title','General_Group', 'second_group','Size','Artist']]
	
	size=[sum(df['Size'])]
	tiers=[5]
	names=['Comics']

	count=5
	lists=['Publisher','Title','General_Group','second_group']
	for i in lists:
		a['Artist']=a.groupby(i)['Size'].transform('sum')
		c=a[['Artist',i]].drop_duplicates()
		names=names+list(c[i])
		size=size+list(c['Artist'])
		count-=1
		tiers=tiers+[count]*len(c)

	n=list(map(str,arange(0,len(names))))
	d={'id':n,'label':names, 'weights':size, 'tiers':tiers}
	p=pd.DataFrame(data=d)
	p.replace(to_replace={'tiers':{1:2}},inplace=True)
	p.dropna(inplace=True)
	new=dict(zip(names,n))
	p.to_csv('nodes.csv', index=None)
	return p,new

def look(series,dic):
	new_list=[]
	for a in series:
		try:
			z=dic[a]
			new_list.append(z)
		except KeyError:
			new_list.append(None)
	return new_list

def edges(df,dic):
	n=df['Publisher'].drop_duplicates() # all publisher names
	p_list=look(n,dic) # publisher indices
	c_list=map(str, map(int,zeros(len(p_list)))) # comic list to index 0 aka 'Comics'

	# edges between publisher and general group
	p=df[['Publisher','General_Group']].drop_duplicates() 
	p.dropna(inplace=True)
	pub_list=look(p['Publisher'],dic)
	gg_list=look(p['General_Group'],dic)

	# edges between General group and 2nd group and Title
	
	m=df[['General_Group','second_group','Title']].drop_duplicates()
	m.dropna(inplace=True)
	
	g1_list=look(m['General_Group'],dic)
	t_list=look(m['second_group'],dic)

	t1_list=look(m['second_group'],dic)
	w_list=look(m['Title'],dic)
	
	#general edges
	m=df[['General_Group','second_group','Title']].drop_duplicates()
	c=m['second_group'].notnull()
	m=m.mask(c)
	m.dropna(how='all',inplace=True)
	
	t2_list=look(m['General_Group'],dic)
	a_list=look(m['Title'],dic)
	
	#m=df[['Writer','Artist']].drop_duplicates()
	a1_list=[]#look(m['Artist'],dic)
	w1_list=[]#look(m['Writer'],dic)
	

	source_list=p_list+pub_list+g1_list+t1_list+t2_list
	tar_list=c_list+gg_list+t_list+w_list+a_list

	newp=['Directed']*len(source_list)

	d={'source':source_list,'target':tar_list, 'type':newp}
	new=pd.DataFrame(data=d)
	new.to_csv('edges.csv',index=None)
	return None

def edges_group(df,dic):
	# edges between publisher and general group
	p=df[['Writer','General_Group','Size','Artist']]#.drop_duplicates()
	p['Artist']=p.groupby(['Writer','General_Group'])['Size'].transform('sum')
	p.drop(axis='columns',labels='Size',inplace=True)
	p.drop_duplicates(inplace=True)
	tar_list=look(p['Writer'],dic)
	source_list=look(p['General_Group'],dic)
	weight=list(p['Artist'])

	un_list=['Undirected']*len(source_list)
	d={'source':source_list,'target':tar_list, 'type':un_list, 'weight':weight}
	k=pd.DataFrame(data=d)
	k.to_csv('edges_group.csv',index=None)
	return None

def edges_pub(df,dic):
	# edges between publisher and general group
	p=df[['Writer','Publisher']]#.drop_duplicates()
	pub_list=look(p['Writer'],dic)
	gg_list=look(p['Publisher'],dic)

	p1=df[['Artist','Publisher']]
	pnew=look(p1['Artist'],dic)
	gnew=look(p1['Publisher'],dic)

	pub_list=pub_list+pnew
	gg_list=gg_list+gnew

	f=pd.DataFrame(data={'source':pub_list,'target':gg_list})
	f.dropna(inplace=True)
	source_list=list(f['source'])
	tar_list=list(f['target'])
	r=zip(source_list,tar_list)

	un_list=['Undirected']*len(source_list)
	d={'source':source_list,'target':tar_list, 'type':un_list, 'weight':None,'ids':r}
	k=pd.DataFrame(data=d)
	k['weight']=k.groupby(['ids']).transform('count')
	k.drop_duplicates(inplace=True)
	k.to_csv('edges_pub.csv',index=None)
	return None

def edges_write(df,dic):
	# edges between publisher and general group
	p=df[['Writer','Artist','Size','Publisher']]#.drop_duplicates()
	p['Publisher']=p.groupby(['Writer','Artist'])['Size'].transform('sum')	
	l=p[['Writer','Artist','Publisher']].drop_duplicates()

	source_list=look(l['Writer'],dic)
	tar_list=look(l['Artist'],dic)
	w_list=l['Publisher']
	un_list=['Undirected']*len(source_list)
	d={'source':source_list,'target':tar_list, 'type':un_list, 'weight':w_list}
	k=pd.DataFrame(data=d)
	k.dropna(inplace=True)
	k.to_csv('edges_write.csv',index=None)
	return k

