#! usr/bin/env python

import sqlite3 as sql
import pandas as pd
import pandas.io.sql as pd_sql

'''Purpose of code is to help catalogue comics in the Comics Folder'''

# Three separate types of files (brackets are optional)

# Regular:   Title, issue, year, author, artist, arc, extention
# Special:   Title, s, arc, year, author, artist, arc, extention
# Collection: Title, col, issue-issue, year, author, artist, arc, extention
# Annual: Title, ann, year, author, artist, arc, extension
# Event: Title, ev, (issue), year, author, artist, extention

#------------------
# .csv folder to update

folder_name='/Users/ksakamoto/Desktop/new_sheet.csv'
data=pd.read_csv(folder_name)

#------------------
# Open database

db=sql.connect('comics.db')
c=db.cursor()
print "Database opened successfully"

#----------------------
# Important queries to remember

# Dataframe object 'data'
# data.ix[int] 
# data.columns

#always on cursor object, always end in ;

# c.execute('''CREATE TABLE tablename(column TYPE, column TYPE);''')
# c.execute ('''DROP TABLE tablename;''')
# c.execute('''SELECT name FROM sqlite_master WHERE type='table';''')
# c.execute('''SELECT * FROM tablename;''')
# c.exectue('''SELECT * FROM tablename LIMIT 1;''')
# null is a python None
# db.commit()
# db.close()

# part of api code
'''
other='&format=json&filter=volume:'+str(volid)+',issue_number:'+str(issue)
field='&field_list=cover_date,id,name,person_credits,story_arc_credits'
field=''
complete_url=url+key+other+field

request=Request(complete_url)
print 'request'
try:
	response=urlopen(request)
	print 'response'
	kittens=response.read()
	print 'read'
	data=json.loads(kittens)
except URLError, e:
	print 'url error'

data=data['results']
sys.exit()'''

#----------------------
# Information

# Title, arc, issue, publisher, writer, read, general group, extension, filename, iss_2, path

# write DataFrame to sql database
#pd_sql.write_frame(data, 'comics2', db)


#----------------------
# Close out database

# commit changes
db.commit()
db.close()


