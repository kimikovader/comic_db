import pandas as pd
import imp
import numpy as np

import pycomic
imp.reload(pycomic)

'''Uploads from .csv to comics objects'''

df1=pd.read_csv('~/Desktop/Comics/comics_db.csv')
df=df1.where((pd.notnull(df1)),None) # replace nan with Nones

def type_handling(x,type):
	'''Makes sure everything goes into the objects as the correct type'''
	if x==None:
		return None
	else:
		return type(x)

def df_to_objects(df):
	'''Pandas Dataframe to list of comic objects'''
	c_list=[]
	for id, vals in df.iterrows():
		comic=pycomic.comic()
		comic.id=int(id)
		comic.title=vals['Title']
		comic.volume=type_handling(vals['Volume'],int)
		comic.issue=type_handling(vals['Issue'],int)
		comic.issue_end=type_handling(vals['Issue_end'],int)
		comic.ctype=vals['Type']
		comic.year=vals['Year']
		comic.arc=vals['Arc']
		comic.publisher=type_handling(vals['Publisher'],str)

		comic.writer=[vals['Writer']]
		comic.artist=[vals['Artist']]
	#	comic.groups=[vals['Group']]
		
	#	comic.characters

		comic.size=vals['Size']
		comic.comments=type_handling(vals['Comments'],str)
		comic.read=np.bool(vals['Read'])
		comic.story_rank=type_handling(vals['Story_Rank'],int)
		comic.art_rank=type_handling(vals['Art_rank'],int)
		
		comic.file_name=vals['File_name']
		comic.path=vals['Path']
		c_list.append(comic)
	return c_list

library=df_to_objects(df)

