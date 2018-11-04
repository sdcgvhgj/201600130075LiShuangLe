def union(l1,l2):
	# 计算两个列表l1和l2的并集
	i = 0
	j = 0
	ans = []
	while i < len(l1) or j < len(l2):
		if i == len(l1):
			ans.append(l2[j])
			j += 1
		elif j == len(l2):
			ans.append(l1[i])
			i += 1
		elif l1[i] < l2[j]:
			ans.append(l1[i])
			i += 1
		elif l1[i] > l2[j]:
			ans.append(l2[j])
			j += 1
		else:
			ans.append(l1[i])
			i += 1
			j += 1
	return ans

def intersect(l1,l2):
	# 计算两个列表l1和l2的交集
	i = 0
	j = 0
	ans = []
	while i < len(l1) and j < len(l2):
		if l1[i] < l2[j]:
			i += 1
		elif l1[i] > l2[j]:
			j += 1
		else:
			ans.append(l1[i])
			i += 1
			j += 1
	return ans

def notto(l,num):
	l.append(num)
	ans = []
	j = 0
	for i in l:
		while j < i:
			ans.append(j)
			j += 1
		j += 1
	return ans

def and_all(lists):
	import heapq
	heap = []
	for i in range(len(lists)):
		heapq.heappush(heap,(len(lists[i]),i))
	while len(heap) >= 2:
		(size,i1) = heapq.heappop(heap)
		(size,i2) = heapq.heappop(heap)
		lists[i1] = intersect(lists[i1],lists[i2])
		heapq.heappush(heap,(len(lists[i1]),i1))
	return lists[heap[0][1]]

def or_all(lists):
	import heapq
	heap = []
	for i in range(len(lists)):
		heapq.heappush(heap,(len(lists[i]),i))
	while len(heap) >= 2:
		(size,i1) = heapq.heappop(heap)
		(size,i2) = heapq.heappop(heap)
		lists[i1] = union(lists[i1],lists[i2])
		heapq.heappush(heap,(len(lists[i1]),i1))
	return lists[heap[0][1]]

def calc(str,inverted_index,num):
	# 根据查询str和inverted-index返回查找结果
	arr = str.split('|')
	for i in range(len(arr)):
		arr[i] = arr[i].split('&')
		for j in range(len(arr[i])):
			arr[i][j] = arr[i][j].strip()
			if arr[i][j][0] == '!':
				arr[i][j] = arr[i][j][1:-1].strip()
				if arr[i][j] in inverted_index.keys():
					arr[i][j] = notto(inverted_index[arr[i][j]],num)
				else:
					arr[i][j] = list(range(num))
			else:
				if arr[i][j] in inverted_index.keys():
					arr[i][j] = inverted_index[arr[i][j]]
				else:
					arr[i][j] = []
		arr[i] = and_all(arr[i])
	return or_all(arr)

def query_test(path,inverted_index):
	from nltk.tokenize import word_tokenize
	f = open(path,'r',encoding='utf-8',errors='ignore')
	arr = []
	for line in f.readlines():
		if line[0:7] == '<query>':
			arr.append(word_tokenize(line[7:-9]))
	
	for i in range(len(arr)):
		lists = []
		for word in arr[i]:
			word = word.strip()
			if word in inverted_index.keys():
				lists.append(inverted_index[word])
			else:
				lists.append([])
		arr[i] = and_all(lists)
		print(i,arr[i])

def main():
	path = r'D:\files\勉強\大三\IR\data\Homework3-tweets\tweets.txt'
	from inverted_index_calculator import calc_inverted_index, get_articles
	articles = get_articles(path)
	num = len(articles)
	inverted_index = calc_inverted_index(articles)
	query_test(r'D:\files\勉強\大三\IR\data\Homework3-tweets\topics.desc.MB171-225.txt',inverted_index)
	return
	s = 'entire & !bomb | ten'
	res = calc(s,inverted_index,num)
	print(res)
	for i in res:
		print(articles[i])

if __name__ == '__main__':
	main()
