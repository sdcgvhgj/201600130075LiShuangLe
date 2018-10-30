def process(articles):
	articles_ = []
	for article in articles:
		articles_.append(word_tokenize(article))
	return articles_

def save_arrays(arrs,path):
	f = open(path,'w')
	for arr in arrs:
		for x in arr:
			f.write(str(x) + ' ')
		f.write('\n')

def get_articles(path):
	import json
	from nltk.tokenize import word_tokenize
	articles = []
	f = open(path,'r')
	for line in f.readlines():
		articles.append(word_tokenize(json.loads(line)['text']))
	return articles

def calc_inverted_index(articles):
	inverted_index1 = {}
	inverted_index2 = {}
	for i in range(len(articles)):
		for word in articles[i]:
			if word not in inverted_index1.keys():
				inverted_index1[word] = set()
			inverted_index1[word].add(i)
	for word in inverted_index1.keys():
		inverted_index2[word] = list(inverted_index1[word])
		inverted_index2[word].sort()
	return inverted_index2

def main():
	path1 = r'D:\files\勉強\大三\IR\data\Homework3-tweets\tweets.txt'
	# path2 = r'D:\files\勉強\大三\IR\data\Homework3-tweets\articles.txt'
	articles = get_articles(path1)
	inverted_index = calc_inverted_index(articles)
	print(len(articles))
	print(articles[1])
	print(inverted_index['ten'])

if __name__ == '__main__':
	main()
