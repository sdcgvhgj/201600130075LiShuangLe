def preprocess(str):
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
	filtered_words = [x for x in stemmed_words if not x in stop_words and x.isalpha()]
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

# print(preprocess("Hello Mr. Smith, how are you doing today? worked The weather is great, and Python is awesome. The sky is pinkish-blue. You shouldn't eat cardboard."))
articles = get_articles(r'D:\files\勉強\大三\IR\20news-18828\alt.atheism')
# print(articles)
processed_articles = [preprocess(x) for x in articles]
# print(processed_articles)
