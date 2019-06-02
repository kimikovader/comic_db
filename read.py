import numpy as np
import pandas as pd

filename='/Users/ksakamoto/Downloads/doc.txt'
filename='/Users/ksakamoto/Documents/thor3.txt'

f=filename.split('/')
j=f[-1].split('.')[0]

file=open(filename,'r')

text=[]
for line in file:
	rude=line.split(' ')
	if rude[-1][-1]=='\n':
		rude[-1]=rude[-1][:-1]
	if rude[0]!=' ' and len(rude)>1:
		r=' '.join(rude)
		text.append(r)
	elif rude[0]!=' ':
		text.append(str(rude[0])) 

names=[]
for line in text:
	if line.isupper()==True:
		names.append(line)

names=np.array(names)
unnames=np.unique(names)
tup=text[0]
new=[]
newp=[]
for line in text[1:]:
	if line.isupper()==True:
		n=' '.join(newp)
		c=n.split(' ')
	
		# get rid of whitespace
		r=[]
		for x in c:
			if x.isspace()==False and len(x)>0:
				r.append(x)
		tups=(tup,n,len(r))
		tup=line	
		newp=[]
		new.append(tups)
		
	else:
		newp.append(line)
	
	

df=pd.DataFrame(data=new, columns=['Character','line','words'])
i=df.groupby('Character')['words'].sum()

word_count=i.sort_values(ascending=False)
line_count=df['Character'].value_counts()

df['exchanges']=df.groupby('Character')['line'].transform('count')

#df.to_csv(j+'.csv')



