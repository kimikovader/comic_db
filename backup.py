import os,sys
from numpy import *
'''This code is to update backup disk with comics folder stuff'''

foldername='/Users/ksakamoto/Desktop/Comics'
#foldername='/Users/ksakamoto/Desktop/comic_art'
#foldername='/Users/ksakamoto/Music/iTunes/iTunes Media/Music'

foldername_b='/Volumes/TRISTRAM/Comics'
#foldername_b='/Volumes/sda1-usb-WD_My_Book_1140_/sakamoto_backup/Comics'
#foldername_b='/Volumes/TRISTRAM/comic_art'
#foldername_b='/Volumes/TRISTRAM/Music'

split=foldername_b.split('/')[-1]

print(foldername, foldername_b)

def full_and_half(foldername):
	full_paths=[]
	for paths,dirs,files in os.walk(foldername):
		for file in files:
			if file[0]!='.':
				full_paths.append(paths+'/'+file)	

	half_paths=[]
	for full in full_paths:
		k=full.split('/')
		k=array(k)
		ind=where(k==split)[0][0]
		c='/'.join(k[ind:])
		half_paths.append(c)
	return full_paths,half_paths

print('Reading Desktop folder...')
a,b=full_and_half(foldername) # new
print('Reading backup folder...')
c,d=full_and_half(foldername_b) # backup

p=in1d(b,d) # of new in backup
pind=where(p==False)[0] 

q=in1d(d,b) # of backup in new
qind=where(q==False)[0]

to_del=array(c)[qind] # these need to be deleted
to_add=array(a)[pind] # these need to be added
to_add_folders=array(b)[pind]
# do stuff from the backup disk

# deleting things
print('Deleting ', len(to_del), ' Files')
print(to_del)
c=input('Waiting for input to commence delete...')
if c=='y':
	for item in to_del:
		k1=item.replace(' ','\ ')
		k1=k1.replace('(','\(')
		k1=k1.replace(')','\)')
		k1=k1.replace('&','\&')
		os.system('rm '+k1)
	print('Finished Deleting.\n')
else:
	print('Not deleting')
#	sys.exit(0)
# adding things
print('Adding ', len(to_add), ' Files')
for am in range(len(to_add)):
	k1=to_add[am].replace(' ','\ ')
	k1=k1.replace('(','\(')
	k1=k1.replace(')','\)')
	k1=k1.replace('&','\&')
	k2=to_add_folders[am].replace(' ','\ ')
	k2=k2.replace('(','\(')
	k2=k2.replace(')','\)')
	k2=k2.replace('&','\&')
	c=k2.split('/')[1:]
	k2='/'.join(c)
	os.system('sudo scp '+ k1 + ' '+foldername_b +'/'+k2)
	print(am, float(am)/len(to_add)*100, '%  ', k1)
print('Done')
