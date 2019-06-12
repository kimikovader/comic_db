import numpy as np
import pandas as pd
import datetime as dt
import codecs
import sys
from pylab import *
import re
from fuzzywuzzy import fuzz, process
import more_itertools as mit

'''Take subtitle file, compare to script/transcript file to amalgamate character, line and times'''

prefix='av4'

# get .csv file
filename='/Users/ksakamoto/Desktop/Comics/codes/words/'+prefix+'.csv'
csv=pd.read_csv(filename)
#sys.exit()
# get subtitle file
filename='/Users/ksakamoto/Desktop/Comics/codes/subs/'+prefix+'_sub.txt'
file=codecs.open(filename,'r',encoding='utf-8', errors='ignore')
file.readline() # skip first integer
first_line=file.readline() # get first timecode
file.seek(0) #go back to top of file

all_lines=file.readlines() # all text

text=[]
p=dt.datetime.strptime(first_line[:8], '%H:%M:%S')
e=dt.datetime.strptime(first_line[17:-6], '%H:%M:%S')
start=p
end=e
newp=[]
for it, line in enumerate(all_lines):
#	text.append(line)
	try:
		int(line)
	except ValueError:
		# Filter spaces and blanks
		if len(line)>1 and line!='\r\n' and line.isupper()==False:
			if line[2]==':': # if a time line
				start=dt.datetime.strptime(line[:8],'%H:%M:%S')\
				+dt.timedelta(milliseconds=int(line[9:12]))
				end=dt.datetime.strptime(line[17:-6],'%H:%M:%S')\
				+dt.timedelta(milliseconds=int(line[26:29]))
				half=(end-start)/2.
			
			line=re.sub('<i>','',line)
			line=re.sub('</i>','',line)
			line=re.sub('\r','',line)
			line=re.sub('\n','',line)

			if line[0]=='-':
			# Deal with double subtitles
				if all_lines[it+1][0]=='-':
					line=line[2:]
					start=start
					end=start+half
				elif all_lines[it-1][0]=='-' and all_lines[it+1][0]=='\r':
					line=line[2:]
					start=end
					end=end+half
				elif all_lines[it-1][0]!='-' and all_lines[it+1][0]=='\r':
					start=start
					end=end
					line=line[2:]
				else:
					start=start
					end=end
					line=line[2:]
					#print(line)
				nq=line.split(' ')
				l=len(nq)
				nw=[]
				for x in nq:
					if len(x)==1 or (x[0]=='I' and x.isalpha()==False) or x.isupper()==False:
						nw.append(x)
				line=' '.join(nw)
				l=len(line.split(' '))
				text.append((start,end, line,l))
				p=start
				e=end
			
			else:
				if start!=p: # if a new time stamp, get all the previous
					n=' '.join(newp)
					ni=n.split(' ')
					l=len(ni)
					text.append((p,e,n,l))
					newp=[]
					p=start
					e=end
				elif start==p:
					#print('a')
					l=line.split(' ')
					k=[]
					for a in l:
						if a.isupper()==False or len(a)==1 or (a[0]=='I' and a.isalpha()==False):
							k.append(a)
					k=' '.join(k)		
					newp.append(k)

series=pd.DataFrame(data=text,columns=['start','end','line','words'])
series=series[series['line']!='']
series['start']=pd.to_datetime(series['start'])
series['end']=pd.to_datetime(series['end'])
#sys.exit()

# fuzzy matching stuff
s=list(series['line'])
d=list(csv[csv.line.isnull()==False])
d1=dict(zip(csv.index[csv.line.isnull()==False],csv.line[csv.line.isnull()==False]))
s1=dict(zip(series.index,series.line))

#sys.exit(0)
#fuzzy_matches = []
#for query in s:
#	best_score = 0
#	best_match = None
#	for index, candidate in d1.items():
#		new_score = fuzz.partial_ratio(query, candidate)
#		if new_score < 80 or new_score < best_score:
#			continue
#		best_score = new_score
#		best_match = candidate
#	fuzzy_matches.append((query, index, best_score))

scores=[]
characters=[]
ind=[]
flags=[]
for count, item in enumerate(s):
	if count%20==0:
		print(count/len(s)*100)
	j=process.extractBests(item,d1,scorer=fuzz.partial_ratio_mod,score_cutoff=75,limit=10)
	if len(j)==1 or (len(j)>0 and (j[0][1]-j[1][1])>2): # you've identified the correct line
		i=j[0][2]
		score=j[0][1]
		char=csv['Character'][j[0][2]]

	elif len(j)>0 and (j[0][1]-j[1][1])<2: # there are so many correct matches
		try:
			old_ind=mit.first_true(ind[::-1]) # get last valid index
			int(old_ind)
		except TypeError:
			old_ind=0
		l=pd.DataFrame(data=j,columns=['line','score','index'])
	
		if any(l['index']==old_ind)==True:
			score=l[l['index']==old_ind]['score']
			i=old_ind
			char=csv['Character'][old_ind]
		elif any(l['index']==old_ind+1)==True:
			score=l[l['index']==old_ind+1]['score']
			i=old_ind+1
			char=csv['Character'][old_ind+1]
		elif any(l['index']==old_ind+2)==True:
			score=l[l['index']==old_ind+2]['score']
			i=old_ind+2
			char=csv['Character'][old_ind+2]
		
		else: # too many matches, can't distinguish
			score=None
			i=None
			char=None
	else: # no matches, or bad matches
		i=None
		score=None
		char=None

	try: # flag the bad data based on (no matches, char==None) or outlier indices
		try:
			ip=int(ind[-1])
		except TypeError:
			ip=0

		if flags[-1]==False and i!=None:
			if abs(i-ip)>5:
				flag=True
				i=None
			else:
				flag=False
		elif flags[-1]==True and i!=None:
			flag=False
		elif i==None:
			flag=True
	except IndexError or TypeError:
		flag=False

	# add all the stats on
	flags.append(flag)
	ind.append(i)
	#print(ind)
	scores.append(score)
	characters.append(char)
series['Character']=characters
series['index']=ind
series['flags']=flags
		
# Find and solve holes

inds=series['index'].interpolate(limit=1,limit_area='inside')
inds_2=inds.apply(lambda x: float(x).is_integer())
inds[inds_2==False]=-999
inds=inds.astype(int)
series['index']=inds

chars=[]
for index in inds:
	try:
		char=csv.iloc[index,1]
	except IndexError:
		char=None
	chars.append(char)
series['Character']=chars
#csv['Character']

series['flags']=False
series['flags'][inds_2==False]=True # unflag interpolated values

# Check and flag non-monotonic values

q=series['index'][inds_2==True]
p=series.index[inds_2==True]

call=[0]
for i, v in enumerate(q[:-1]):
	if (v-call[-1])>0 and (v-q.iloc[i+1])>0:
		series['flags'][p[i]]=True
	elif abs(v-call[-1])>12:
		print(i,v)
		series['flags'][p[i]]=True
	else:
		call.append(v)





