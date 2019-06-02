import numpy as np
import pandas as pd
import re

filename='/Users/ksakamoto/Documents/kk/iron1.txt'
#filename='/Users/ksakamoto/Documents/kk/bp.txt'


f=filename.split('/')
j=f[-1].split('.')[0]

file=open(filename,'r')
text=[]
# .html cleanup stuff
#for line in file:
#	text.append(line)
#	if  line[35:38]=='180' or line[35:38]=='266':# or line[35:38]=='174' or line[35:38]=='245' or line[35:38]=='246' or line[35:38]=='244':# or line[30:38]=='left:149':
#		text.append(line[95:])
	#text.append(line[35:38])
#m=[]
#for x in text:
#	try:
#		p=int(x)
#		m.append(p)
#	except ValueError:
#		pass
#series=pd.Series(m)
#c=series.value_counts()

#filenew=open(j+'.txt','w')
#for a in text:
#	filenew.write(a)
#filenew.close()

text=[]
for line in file:
#	print('a')
	text.append(line)
tup=text[0][:-1]
new=[]
newp=[]
for line in text[1:]:
	if line.isupper()==True:
		n=' '.join(newp)
		n=re.sub('\n','',n)
		c=n.split(' ')
		r=[]
		for x in c:
			if x.isspace()==False and len(x)>0:
				r.append(x)	
		new.append((tup.lstrip(),n[:-1], len(r)))
		newp=[]
		tup=line[:-1]
	else:
		newp.append(line)
		
df=pd.DataFrame(data=new, columns=['Character','line','words'])
i=df.groupby('Character')['words'].sum()

word_count=i.sort_values(ascending=False)
line_count=df['Character'].value_counts()


df['exchanges']=df.groupby('Character')['line'].transform('count')

df.to_csv(j+'.csv')



