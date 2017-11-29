#! /usr/bin/env python

import pandas as pd
from numpy import *
import os, sys
import datetime

'''Allows searching of the DataFrame comics file.'''

#-----------------
# To and from .csv
#----------------

def load_comics(filename='~/Desktop/Comics/comics_db.csv'):
	'''Loads csv via Pandas of *filename'''
	df=pd.read_csv(filename)
	return df

def save_csv(df,filename):
	'''df to .csv stuff'''
	order=['Title','Arc','Writer','Volume','Issue','Comments','Read','Story_Rank','Art_rank','Artist','Group', 'General_Group','second_group','Publisher','File_name','Path','Size','Type','Year','Month 1','Month 2','Extension','Issue_end']
	filename='/Users/ksakamoto/Desktop/Comics/'+filename
	df.to_csv(filename,columns=order,index=None)
	return 0

def save_and_backup(df, filename='comics_db.csv'):
	'''Saves and backups the .csv file if wanted'''
	c=input('Save Dataframe to '+ filename +'? y/n ')
	if c=='y':
		today=datetime.datetime.today()
		# save the old_csv file
		newname=str(today).split(' ')[0]+'_comics_db.csv'
		os.system('mv ~/Desktop/Comics/comics_db.csv ~/Desktop/Comics/old_data/'+newname)
		save_csv(df,filename)
		print('DataFrame saved in ' + filename)
	else:
		print('DataFrame NOT saved')
	return 0 		 	

#---------------
# Miscellaneous
#--------------

def filt_by_cats(data_object, list_of_cats):
	'''data_object==DataFrame, list_of_cats==list of DataFrame columns to filter unique entries by'''
	new_object=data_object[list_of_cats]	
	c=new_object.drop_duplicates()
	new=c.sort('Title')
	return new
	
def artist_list(data):
	'''For fun these are the unique artists in the 'art is awesome' tag'''
	artists=data.query('Art_rank==1')['Artist']
	d=pd.value_counts(artists)
	return d

def writer_list(df, rank=0):
	'''Writer frequency with ranking > ranking'''
	writers=df.query('Story_Rank>=@rank')#,'Size']
	c=writers.groupby('Writer')['Size'].sum()
	c.sort_values(inplace=True, ascending=False)
	return c

#-----------------
# Search function
#----------------

def search(df,**kwargs):
	'''Search comic dataframe object (df). Keywords: w=writer, g=group, a=artist, type=comic type, read=1 or 0, arc=arc, p=publisher, t=title, art=1 or 0, rank=1 to 10, c=comments (True or False), all_entries=boolean.'''
	inds=[]
	comments=False
	all_entries=False
	count=0
	new_keys={'w':'Writer','g':'Group','a':'Artist','type':'Type','read':'Read','arc':'Arc','p':'Publisher','t':'Title','art':'Art_rank','rank':'Story_Rank','c':'Comments'}
	for key, value in kwargs.iteritems():
		if key=='w' or key=='a' or key=='arc':
			value=value.lower()
		if key=='read' and value!=1:
			for item in where(df['Read'].isnull()==True)[0]:
				inds.append(item)
			#print inds
		elif key=='c':
			comments=True
			count-=1
		elif key=='all':
			all_entries=True
			count-=1
		else:
			proc=new_keys[key]+'==@value'
			for item in array(df.query(proc).index):
				inds.append(item)
		count+=1
	n=pd.Series(inds)
	n=pd.value_counts(n)
	w=n.index[where(n==count)]
	new=df.ix[w]
	if len(new)<1:
		print('\nNo comics matching those parameters found.\n')
		
	else:
		print('\n', len(new),' comics matching parameters found.')
		lis=['Title','Writer','Artist','Arc']
		if comments==True:
			lis.append('Comments')
		if all_entries==True:
			news=new[lis]
		else:
			news=new[lis].drop_duplicates(subset=['Title','Writer','Arc'])
			news=news.drop_duplicates(subset=['Title','Writer','Artist'])
		news=news.sort_values(by=['Title','Writer'])
		m,text=display_text(news)
		lis=['Index']+lis
		k=[lis[i].ljust(m[i]) for i in range(0,len(lis))]
		h='\t'.join(k)
		print('\n', h, '\n')
		for i in text:
			print(i)
	return None

def comic(df,ind):
	filename=df.ix[ind]
	os.system('open '+filename['Path'])
	return None

def display_text(objec):
	ix=array(map(str,objec.index))
	multi_array=list(array(objec).transpose())
	multi_array=multi_array[::-1]
	multi_array.append(ix)
	multi_array=multi_array[::-1]
	multi_array=array(multi_array).transpose()
	(a,b)=multi_array.shape
	ms=[]
	text=[]
	for i in range(0,b):
		multi_array[:,i]=map(str,multi_array[:,i])
		m=max(map(len,multi_array[:,i]))
		c=where(multi_array[:,i]=='nan')[0]
		if len(c)>0:
			multi_array[c,i]=''
		if m>15:
			ms.append(m)
		else:
			m=15
			ms.append(15)
		multi_array[:,i]=[p.ljust(m) for p in multi_array[:,i]]
	
	for x in range(0,a):
		text.append('\t'.join(multi_array[x]))
	return ms,text

def story(data, ranking=None):
	'''Returns printed list of comic stories ranked 'ranking' or higher. 1 argument==rankingINT between 1 and 10, defaults to 0.'''
	if ranking==None:
		ranking=0.
	print('\nStory Rankings equal to greater than: ', str(int(ranking)))
	m,text=display_text(filt_by_cats(story_rank(data,ranking),['Story_Rank','Title','Writer','Arc']))
	k=['Rank'.ljust(m[0]),'Title'.ljust(m[1]),'Writer'.ljust(m[2]),'Arc'.ljust(m[3])]
	h='\t'.join(k)
	print('\n', h, '\n')
	for i in text:
		print(i)
	return 0

def art(data):
	'''Returns printed list of comic stories with the art tag.'''
	print('\nMarked with the Art Tag, alphabetical by title.\n')
	m,text=display_text(filt_by_cats(art_ranked(data), ['Title','Writer','Artist','Arc']))
	k=['Title'.ljust(m[0]),'Writer'.ljust(m[1]),'Artist'.ljust(m[2]),'Arc'.ljust(m[3])]
	h='\t'.join(k)
	print(h, '\n')
	for i in text:
		print(i)
	return 0

def read_and_sort(folder_name):
	'''Reads all the comic files in foldername and sorts by filename. Returns a dataframe.'''	
	full_path=[]
	count=0

	# Initializing
	titles=[]
	writers=[]
	artists=[]
	arcs=[]
	comtypes=[]
	years=[]
	sizes=[]
	publishers=[]
	issues=[]
	issues_end=[]
	paths=[]
	folders=[]
	
	print('\nScanning folder...')
	for path, dirs, files in os.walk(folder_name):
		for file in files:
			if file[0]!='.' and file[-2]=='b':
				full_path=path+'/'+file
				publisher=full_path.split('/')[5]
				size=os.stat(full_path).st_size*10**(-6) # size of file in MB
				orange=file.split('.')
				orange=orange[0].split('_')
				if 'mini' in orange:
                                	index=orange.index('mini')
                                	comtype=4
                                	title=' '.join(orange[:index])
                                	year=orange[index+2]
                                	iss=orange[index+1]
                                	writer=orange[index+3]
                                	artist=orange[index+4]
                                	arc=' '.join(orange[index+5:])
                                	iss2=None
				elif 'ev' in orange:
                                  	index=orange.index('ev')
                                  	comtype=3
                                  	num=int(orange[index+1])
                                  	if num>1000:
                                        	year=orange[index+1]
                                        	iss=None
                                  	else:
                                        	iss=orange[index+1]
                                        	year=orange[index+2]
                                  	writer=orange[-2]
                                  	title=' '.join(orange[:index])
                                  	artist=orange[-1]
                                  	iss2=None
                                  	arc=title.lower()
				elif 's' in orange:
                                  	index=orange.index('s')
                                  	comtype=2
                                  	title=' '.join(orange[:index])
                                  	year=orange[index+1]
                                  	iss=None
                                  	iss2=None
                                  	writer=orange[index+2]
                                  	artist=orange[index+3]
                                  	arc=' '.join(orange[index+4:])
				elif 'ann' in orange:
                                	index=orange.index('ann')
                                	comtype=1
                                	title=' '.join(orange[:index])
                                	year=orange[index+1]
                                	iss=None
                                	iss2=None
                                	writer=orange[index+2]
                                	artist=orange[index+3]
                                	arc=' '.join(orange[index+4:])
				elif 'col' in orange:
                                  	index=orange.index('col')
                                  	comtype=5
                                  	title=' '.join(orange[:index])
                                  	iss=orange[index+1]
                                  	iss2=orange[index+2]
                                  	year=orange[index+3]
                                  	writer=orange[index+4]
                                  	artist=orange[index+5]
                                  	arc=' '.join(orange[index+6:])
				else:
                                  	comtype=0
                                  	for i in orange:
                                          	try:
                                                  	j=int(i)
                                                  	if j>1000:
                                                          	year=str(j)
                                          	except ValueError:
							#print i
                                                  	pass
                                  	index=orange.index(year)
                                  	iss=orange[index-1]
                                  	iss2=None
                                  	title=' '.join(orange[:index-1])
                                  	writer=orange[index+1]
                                  	artist=orange[index+2]
                                  	arc=' '.join(orange[index+3:])
				
				# put them all in strands	
				titles.append(title)
				comtypes.append(comtype)
				years.append(year)
				issues.append(iss)
				issues_end.append(iss2)
				writers.append(writer)
				artists.append(artist)
				arcs.append(arc)
				publishers.append(publisher)
				folders.append(file)
				paths.append(full_path)
				sizes.append(size)
				
			else:
				if file[0]!='.':
					count+=1
	print('Scanned: ', len(arcs), ' files.')
	print('Skipped: ', count, ' files.')
 
	new_data=[titles,comtypes,years,issues,issues_end,writers,artist,arcs,publishers,folders,paths,sizes]		
	print('Done.')
 	
	#Make new DataFrame
	cats=['Title','Type','Year','Issue','Issue_end','Writer','Artist','Arc','Publisher','File_name','Path','Size']
	others=['Volume', 'Month 1', 'Month 2', 'Group','General_Group','second_group', 'Comments','Read', 'Story_Rank','Art_rank']
	cats+=others
	none_list=list([None]*len(new_data)) # dummy blank data to put in DF
	new_data+=len(others)*none_list
	dic=dict(zip(cats,new_data))
 
	df=pd.DataFrame(data=dic) # New Dataframe but with incomplete information
	return df
