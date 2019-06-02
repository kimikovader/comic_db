import pandas as pd
import sys, os
import numpy as np

df1=pd.read_csv('/Users/ksakamoto/Desktop/Comics/codes/cap.csv',index_col='Title')
cols=df1.columns[2:]
c_fun=['av4','cm','ant2','av3','bp','thor3','sm','gotg2','strange','cap3','ant1','av2','gotg1','cap2','thor2','iron3','av1','cap1','thor1','iron2','incredible_hulk','iron1']
j=list(zip(c_fun,cols))
j=dict(j)

dic={"T'chaka":'Tchaka','Peter':'Parker','Toomes':'Vulture','Michelle':'MJ','Liz ':'Liz','Justin':'Hammer','Ivan':'Whiplash','Agent coulson':'Coulson','The collector':'Collector','Yondu udonta':'Yondu',"N'jobu":'Njobu','Bucky':'Barnes',"W'kabi":'Wkabi','Red skull':'Red Skull','Bucky barnes':'Barnes',"M'baku":'Mbaku','Secretary ross':'Ross','Proxima midnight':'Midnight','Pepper potts':'Pepper',"T'challa":'Tchalla','Peter parker':'Parker','Ebony maw':'Maw','Peter quill':'Quill','James rhodes':'Rhodey','Wanda maximoff':'Wanda','Nick fury':'Fury','Bruce banner':'Bruce','Tony stark':'Tony','Natasha romanoff':'Widow','Clint barton':'Hawkeye','Scott lang':'Scott', 'Dr. hank pym':'Hank', 'Darren cross':'Cross', 'Hope van dyne':'Hope','Cassie lang':'Cassie','Sam wilson':'Sam','Howard stark':'Howard','Peggy carter':'Peggy','Steve rogers':'Cap','Banner':'Bruce','Natasha':'Widow','Steve':'Cap','Maria hill':'Hill','Hulk':'Bruce','Jane foster':'Jane','Darcy lewis':'Darcy','Erik selvig':'Selvig'}


sers=[]
for root, dirs, files in os.walk(top='/Users/ksakamoto/Desktop/Comics/codes/words'):
	for file in files:
		name=file.split('.')[0]
		if len(name)>0:
			truename=j[name] #get real name from dictionary above
			sers.append((truename,pd.read_csv(root+'/'+file,index_col=['Unnamed: 0'])))

series=pd.DataFrame(data=sers,columns=['Movie','Series'])

df=df1.copy(deep=True)
df.iloc[3:,2:]=0.
total_words=[]
for count in range(0,len(series)):
	s=series.loc[count]
	name=s['Movie']
	words=sers[count][1]['words'].sum()
	total_words.append((name,words))
	p=s['Series'].groupby('Character')['words'].sum()
	df.loc['Runtime',name]=words
	p=p.sort_values(ascending=False)
	char_names=[]
	for item in p.index:
		char_names.append(item[0].upper()+item[1:].lower())
	dist=list(zip(char_names,p.index))
	for a,b in dist:
		if any(df.index.isin([a]))==True:
			df.loc[a,name]+=p.loc[b]
		#	print(a)
		else:
			try:
				n=dic[a]
				df.loc[n,name]+=p.loc[b]
			except KeyError:
				pass

tot_words=pd.DataFrame(data=total_words,columns=['Movie','words'])
df=df.drop(columns=['Captain Marvel','Doctor Strange','Iron Man 3','Endgame','Ant-Man & the Wasp'])
#df=df.T[df.T.Group=='']
#df=df.T
##df2=df1.iloc[2:,:].apply(pd.to_timedelta)
d=df.iloc[2:,:]
d.replace(0, np.nan,inplace=True)
#d.dropna(how='all',inplace=True)
#char_tot=d.T.sum()/tot_words['words'].sum()*100
#sys.exit()

#df1=df1.T[df1.T.Group==None]
#df1=df1.T
#df2=df1.iloc[2:,:].apply(pd.to_timedelta)
#df2=df1.iloc[2:,2:].apply(pd.to_timedelta)
#tot=df2.loc['Runtime'].sum()
#df2.dropna(how='all',inplace=True)
#char_tot=df2.T.sum()/tot*100
#sys.exit()

#df=df.T[df.T.Group=='Team']
df1=df1.drop(columns=['Captain Marvel','Doctor Strange','Iron Man 3','Endgame','Ant-Man & the Wasp'])
#df1=df
chars=df1.iloc[3:,2:]
chars=chars.apply(pd.to_timedelta)
char_tot=pd.to_numeric(chars.T.sum())/1E9/60
runs=pd.to_numeric(pd.to_timedelta(df1.loc['Runtime']))[2:]/1E9/60
n=df.iloc[3:,2:]
n1=n.T.sum()
by_mov=n.sum()/runs
by_char=n1/char_tot	




