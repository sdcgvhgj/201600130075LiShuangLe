def union(l1,l2):
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

def calc(str,inverted_index):
	str = str.strip()
	# print(str)
	ans = []
	if '|' in str:
		for s in str.split('|'):
			ans = union(ans,calc(s,inverted_index))
	elif '&' in str:
		res = []
		for s in str.split('&'):
			res.append(calc(s,inverted_index))
		ans = res[0]
		for r in res:
			ans = intersect(ans,r)
	else:
		if str in inverted_index.keys():
			ans = inverted_index[str]
	return ans

def main():
	path = r'D:\files\勉強\大三\IR\data\Homework3-tweets\tweets.txt'
	from inverted_index_calculator import calc_inverted_index, get_articles
	articles = get_articles(path)
	print(articles[384])
	inverted_index = calc_inverted_index(articles)
	s = 'fuck | shit'
	res = calc(s,inverted_index)
	print(res)
	for i in res:
		print(articles[i])

if __name__ == '__main__':
	main()
