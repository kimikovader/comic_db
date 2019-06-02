import pandas as pd
import imp
import numpy as np
import postgres
import odo

import pycomic
imp.reload(pycomic)

'''Uploads from .csv to comics objects, then goes into db'''

# get list of comics objects from .csv

df1=pd.read_csv('~/Desktop/Comics/comics_db.csv')
df=df1.where((pd.notnull(df1)),None) # replace nan with Nones
library=pycomic.df_to_objects(df)

# initialize Database

db=postgres.Postgres('postgresql://postgres:diomedes@localhost/test')

# DB table already created, you have been warned
#db.run('CREATE TABLE comics (title varchar(80), volume int, issue int, issue_end int, year int, arc varchar(80), publisher varchar(30), size real, comments varchar(120), read bool, story_rank real, art_rank bool, filename varchar(80), path varchar(120));')	

#db.run('CREATE TABLE stupid (x varchar(90), y INT);')

#db.run('COPY comics (title) FROM /Users/ksakamoto/Destop/Comics/comics_db.csv WITH csv')

fil='/Users/ksakamoto/Documents/comics.csv'
f=odo.resource(fil)
dshape=odo.discover(f)

t=odo.odo(fil, 'postgresql://postgres:diomedes@localhost/test::comics', dshape=dshape)

