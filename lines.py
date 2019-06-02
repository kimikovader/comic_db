import pandas as pd

filename='~/Desktop/Comics/codes/Thor3.csv'
df=pd.read_csv(filename,index_col=0)

# find unique characters
chars=pd.Series(df.iloc[:,2:].values.ravel()).unique()[1:] # drop nan

# search whole dataframe for symbol
tup=[]
for char in chars:
	spec=df.loc[df.isin(['T']).any(axis=1)]
	times=pd.to_datetime(spec.index)
	tup.append((char,times))
