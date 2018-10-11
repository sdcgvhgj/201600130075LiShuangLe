def get_articles(path,percentage): # 读取文章
	from nltk.tokenize import word_tokenize
	from nltk.corpus import stopwords
	from nltk.stem import PorterStemmer	
	stop_words = set(stopwords.words('english'))
	ps = PorterStemmer()

	import os
	train_articles = {}
	test_articles = {}
	for topic in os.listdir(path):
		path2 = os.path.join(path,topic)
		articles1 = []
		articles2 = []
		i = 0
		num = len(os.listdir(path2))
		for article in os.listdir(path2):
			f = open(os.path.join(path2,article),'rb')
			article1 = f.read().decode('utf-8','ignore')

			normalized_words = [''.join(filter(str.isalpha,word.lower())) for word in word_tokenize(article1)]
			stemmed_words = [ps.stem(x) for x in normalized_words]
			filtered_words = [x for x in stemmed_words if x and not x in stop_words]
			words = filtered_words
			if(i < percentage * num):
				articles1.append(words)
			else:
				articles2.append(words)
			i += 1
		train_articles[topic] = articles1
		test_articles[topic] = articles2
		print(topic + ' ' + str(num))
	for topic in train_articles.keys():
		print(topic + ' ' + str(len(train_articles[topic])) + ':' + str(len(test_articles[topic])))
	return (train_articles,test_articles)

def calc_freq(topics): # 统计词频
	count = {}
	for topic in topics.keys():
		count_topic = {}
		for article in topics[topic]:
			for word in article:
				if not word in count_topic.keys():
					count_topic[word] = 0
				count_topic[word] += 1
		count[topic] = count_topic
	return count

def classify(train_articles,test_articles):
	import math
	count = calc_freq(train_articles)
	
	words_in_topics = {}
	all_words = set()
	for topic in count.keys():
		words_in_topics[topic] = 0
		for word in count[topic].keys():
			all_words.add(word)
			words_in_topics[topic] += count[topic][word]
	print(len(all_words))

	results = {}
	for topic in test_articles.keys():
		result = []
		for article in test_articles[topic]:
			max_p = - float('inf')
			for test_topic in train_articles.keys():
				p = 0.0
				for word in article:
					if not word in count[test_topic].keys():
						count[test_topic][word] = 0
					p += math.log(count[test_topic][word] + 0.1) - math.log(words_in_topics[test_topic] + 0.1*len(all_words))
				p += math.log(len(train_articles[test_topic]))
				if p > max_p:
					max_p = p
					ans = test_topic
			result.append(ans)
		results[topic] = result
	return results

def check_result(results):
	oks = 0
	nums = 0
	for topic in results.keys():
		ok = 0
		num = len(results[topic])
		for result in results[topic]:
			if result == topic:
				ok += 1
		print(topic + ' ' + str(ok) + ' in ' + str(num) + ' ' + str(1.0*ok/num*100) + '%')
		oks += ok
		nums += num
	print(str(oks) + ' ' + str(nums) + ' ' + str(1.0*oks/nums*100) + '%')

if __name__ == '__main__':
	# articles = read_arrays(r'D:\files\勉強\大三\IR\Homework\Homework 1 VSM\processed_articles.txt')
	articles = get_articles(r'D:\files\勉強\大三\IR\20news-18828',0.8)
	result = classify(articles[0],articles[1])
	check_result(result)
	# 正确率 86.37935621175845%