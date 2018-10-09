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
				vector.append(tf[word] * idf[word])
			else:
				vector.append(0.0)
		vectors.append(vector)
	return vectors

def calc_distance(vec1,vec2):
	# Cosine Similarity
	dot = 0.0
	d1 = 0.0
	d2 = 0.0
	for i in range(len(vec1)):
		x1 = float(vec1[i])
		x2 = float(vec2[i])
		d1 += x1 * x1
		d2 += x2 * x2
		dot += x1 * x2
	import math
	return dot / math.sqrt(d1) / math.sqrt(d2)

if __name__ == '__main__':
	from preprocess import read_arrays, save_arrays
	articles = read_arrays('processed_articles.txt')
	vectors = calc_vector(articles)
	# print(calc_distance(vectors[0],vectors[1]))
	save_arrays(vectors,'vectors.txt')