
def process(str):
	from nltk.tokenize import word_tokenize
	from nltk.corpus import stopwords
	from nltk.stem import PorterStemmer
	
	# Tokenization
	tokenized_words = word_tokenize(str)	
	
	# Stemming and Normalization
	ps = PorterStemmer()
	stemmed_words = [ps.stem(x) for x in tokenized_words]
	
	# Stopword Filtering
	stop_words = set(stopwords.words('english'))
	def has_alpha(str):
		for x in str:
			if(x.isalpha()):
				return True
		return False
	filtered_words = [x for x in stemmed_words if not x in stop_words and has_alpha(x)]
	
	return filtered_words

def get_articles(path):
	import os
	articles = []
	if os.path.isfile(path):
		f = open(path,'rb')
		articles.append(f.read().decode('utf-8','ignore'))
		f.close()
		return articles
	for file in os.listdir(path):
		file_path = os.path.join(path, file)
		if os.path.isdir(file_path):
			articles.extend(get_articles(file_path))
		if os.path.isfile(file_path):
			f = open(file_path,'rb')
			articles.append(f.read().decode('utf-8','ignore'))
			f.close()
	return articles

def save_arrays(arrs,path):
	f = open(path,'w')
	for arr in arrs:
		for x in arr:
			f.write(str(x) + ' ')
		f.write('\n')

def read_arrays(path):
	f = open(path,'r')
	arrs = []
	for line in f.readlines():
		arrs.append(line.split())
	return arrs

if __name__ == '__main__':
	articles = get_articles(r'D:\files\勉強\大三\IR\20news-18828\alt.atheism')
	processed_articles = [process(x) for x in articles]
	save_arrays(processed_articles,'processed_articles.txt')