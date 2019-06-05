import pandas as pd
import numpy as np

'''Clean transcript format.'''

filename='/Users/ksakamoto/Desktop/Comics/codes/scripts/strange.txt'
file=open(filename,'r')

j=filename.split('/')[-1]
j=j.split('.')[0]

text=[]
for line in file:
	ind=line.find('[')
	ind2=line.find(']')
	if ind!=-1:
		line=line[:ind]+line[ind2+1:]
#	if len(line)>1:
#		if line[2]=='\t':
#			text.append(line[3:])
#	elif len(line)>0 and line[0]!='\n':
#		print('o')
#		text.append(line[:])
		text.append(line)	
	elif ind==-1:
		text.append(line)
print(len(text))			

f=open(j+'.txt','w')
for x in text:
	f.write(x)
f.close()	
 

