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

def calc(str,inverted_index):
	# 根据查询str和inverted-index返回查找结果
	str = str.strip()
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
	inverted_index = calc_inverted_index(articles)
	s = input("input : ")
	res = calc(s,inverted_index)
	print(res)
	for i in res:
		print(articles[i])

if __name__ == '__main__':
	main()
