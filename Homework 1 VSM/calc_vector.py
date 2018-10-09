def calc_idf(articles):
	import math
	df = {}
	for article in articles:
		for word in set(article):
			if not word in df.keys():
				df[word] = 0
			df[word] += 1
	idf = {}
	for word in df.keys():
		idf[word] = math.log(len(articles)) - math.log(df[word])
	return idf

def calc_tf(articles):
	tf = []
	for article in articles:
		c = {}
		for word in article:
			if not word in c.keys():
				c[word] = 0.0
			c[word] += 1.0
		tf.append(c)
	return tf

def calc_vector(articles):
	tfs = calc_tf(articles)
	idf = calc_idf(articles)
	all_words = set()
	for article in articles:
		all_words.update(article)
	# print(all_words)
	vectors = []
	for tf in tfs:
		vector = []
		for word in all_words:
			if word in tf.keys():
				vector.append(tf[word]*idf[word])
			else:
				vector.append(0.0)
		vectors.append(vector)
	return vectors

# print(calc_vector([['sadf','asdf','asdf'],['sdf']]))
# print(calc_idf([['sadf','asdf'],['sadf']]))
articles = []
f = open('processed_articles.txt','r')
for line in f.readlines():
	articles.append(line.split())
vectors = calc_vector(articles)
f = open('vectors.txt','w')
for vector in vectors:
	for value in vector:
		f.write(' ' + str(value))
	f.write('\n')