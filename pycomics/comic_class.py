# Defines the comic class and associated methods

class comic():
	'''
	Comic attributes:
	title (string)
	volume (int)
	issue (int)
	issue_end (int)
	ctype (int)
	year (int)
	arc (string)
	publisher (string)

	writer (array of strings)
	artist (array of strings)
	groups (array of strings)
	characters (array of strings)

	id (int)	
	size (float)
	comments (string)
	read (boolean)
	story_rank (int)
	art_rank (boolean)
	
	file_name (string)
	path (string)'''

	title=None
	volume=None
	issue=None
	issue_end=None
	ctype=None
	year=None
	arc=None
	publisher=None

	writer=[]
	artist=[]
	groups=[]
	characters=[]

	id=None
	size=None
	comments=None
	read=False
	story_rank=None
	art_rank=None
	
	file_name=None
	path=None

	def __iter__(self):
		for attr, value in self.__dict__.items():
			yield attr, value

	def to_dict(self):
		return {key: value for (key, value) in self}	
