
file='/Users/ksakamoto/Documents/kk/iron3.txt'

f=open(file,'r')
text=f.readlines()

new_text=[]
for line in text:
	l=line.split(' ')
	if l[0][-1]==':' and l[0].isupper()==True:
		line=' '.join(l[1:])
		#print(line)
		new_text.append(line)
		#print(line)
	elif line.isupper()!=True:
		new_text.append(line)
		#pass
j=open('iron3_new.txt','w')
for line in new_text:
	j.write(line)

j.close()
	
