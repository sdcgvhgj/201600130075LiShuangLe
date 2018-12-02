def get_tweets(path):
	# 读取json格式的tweet并提取其内容并返回分词后结果
	import json
	from nltk.tokenize import word_tokenize
	tweets = []
	f = open(path,'r',encoding='utf-8',errors='ignore')
	for line in f.readlines():
		tweets.append((json.loads(line)['tweetId'], word_tokenize(json.loads(line)['text'])))
	return tweets

def get_querys(path):
	from nltk.tokenize import word_tokenize
	f = open(path,'r',encoding='utf-8',errors='ignore')
	arr1 = []
	arr2 = []
	for line in f.readlines():
		if line[0:5] == '<num>':
			arr1.append(line[16:-8])
		if line[0:7] == '<query>':
			arr2.append(word_tokenize(line[7:-9]))
	arr = []
	for i in range(len(arr1)):
		arr.append((arr1[i],arr2[i]))
	return arr

def calc_inverted_index(tweets):
	num = len(tweets)
	
	#calculate avdl
	avdl = 0
	for tweet_id, tweet in tweets:
		avdl += len(tweet)
	avdl = 1.0 * avdl / num

	#calculate df
	df = {}
	for tweet_id, tweet in tweets:
		for word in tweet:
			if word not in df.keys():
				df[word] = 0
			df[word] = df[word] + 1

	#calculate inverted_index
	inverted_index = {}
	for tweet_id, tweet in tweets:
		for word in tweet:
			if word not in inverted_index.keys():
				inverted_index[word] = {}
			if tweet_id not in inverted_index[word].keys():
				inverted_index[word][tweet_id] = 0
			inverted_index[word][tweet_id] += 1

	#calculate doc_len
	doc_len = {}
	for tweet_id, tweet in tweets:
		doc_len[tweet_id] = len(tweet)
	return (num,avdl,df,inverted_index,doc_len)

def BM25(M,avdl,df,inverted_index,doc_len,querys,k,b):
	ans = []
	for query_id,query in querys:
		#calculate counts of words in the query
		cnt = {}
		for word in query:
			if word not in cnt.keys():
				cnt[word] = 0
			cnt[word] = cnt[word] + 1

		score = {}
		#calculate scores
		import math
		for word in cnt.keys():
			if word not in inverted_index.keys():
				continue
			for tweet_id,num in inverted_index[word].items():
				if tweet_id not in score.keys():
					score[tweet_id] = 0
				score[tweet_id] += cnt[word] * (k + 1) * num / (num + k * (1 - b + b * doc_len[tweet_id] / avdl)) * math.log(1.0 * (M + 1) / df[word])
		# print(score)
		res = []
		for tweet_id,value in score.items():
			res.append((value,tweet_id))
		res.sort(reverse = True)
		# print(res)
		for term in res:
			ans.append((query_id,term[1]))
	return ans

def write_result(path,res):
	f = open(path,'w',encoding='utf-8',errors='ignore')
	for term in res:
		f.write(term[0] + ' ' + term[1] + '\n')

if __name__ == '__main__':
	tweets = get_tweets('tweets.txt')
	querys = get_querys('topics.desc.MB171-225.txt')
	(num,avdl,df,inverted_index,doc_len) = calc_inverted_index(tweets)
	ans = BM25(num,avdl,df,inverted_index,doc_len,querys,100,0.5)
	write_result('result.txt',ans)
	#result : MAP = 0.44820987854433175, NDCG = 0.6521315470248232
