import pandas as pd
import re

'''Read transcript format in and output a .csv'''

filename='/Users/ksakamoto/Desktop/Comics/codes/scripts/av4.txt'
#filename='/Users/ksakamoto/Documents/gotgp.txt'

file=open(filename,'r')
j=filename.split('/')[-1]
j=j.split('.')[0]

text=[]
for line in file:
	text.append(line[:])

new=[]
for line in text:
	lines=line.split('\u2028')
	for a in lines:
		ind=a.find(':')
		if ind!=-1:
			lip=a[ind+1:].lstrip()
			lip=lip.rstrip()
			lip=re.sub('\n','',lip)
			j1=lip.split(' ')
			j1=list(filter(None,j1))
			new.append((a[:ind],lip,len(j1)))
		#else:
			#print(a)

df=pd.DataFrame(data=new,columns=['Character','line','words'])
i=df.groupby('Character')['words'].sum()

word_count=i.sort_values(ascending=False)
line_count=df['Character'].value_counts()

df['exchanges']=df.groupby('Character')['line'].transform('count')
df.to_csv(j+'.csv')

