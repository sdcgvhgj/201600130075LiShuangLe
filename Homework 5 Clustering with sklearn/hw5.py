import json

def read(file_name):
	X = []
	Y = []
	with open(file_name, 'r', errors='ignore') as f:
		for line in f:
			obj = json.loads(line.strip())
			X.append(obj['text'])
			Y.append(obj['cluster'])
	return X, Y

def nmi_eval(Y,Y_):
	from sklearn.metrics import normalized_mutual_info_score 
	return normalized_mutual_info_score(Y, Y_, average_method='arithmetic')

def feature_extract(X):
	from sklearn.feature_extraction.text import TfidfVectorizer
	vectorizer = TfidfVectorizer()
	return vectorizer.fit_transform(X).toarray()

def test_KMeans(X,Y):
	from sklearn.cluster import KMeans
	Y_ = KMeans(len(set(Y))).fit_predict(X)
	print('k-means :', nmi_eval(Y,Y_))

def test_AffinityPropagation(X,Y):
	from sklearn.cluster import AffinityPropagation
	af = AffinityPropagation().fit(X)
	Y_ = af.labels_
	print('affinity propagation :', nmi_eval(Y,Y_))

def test_MeanShift(X,Y):
	from sklearn.cluster import MeanShift, estimate_bandwidth
	bandwidth = estimate_bandwidth(X)
	ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
	ms.fit(X)
	Y_ = ms.labels_
	# print(Y_)
	print('mean shift :', nmi_eval(Y,Y_))

def test_SpectralClustering(X,Y):
	from sklearn.cluster import SpectralClustering
	sc = SpectralClustering(n_clusters=len(set(Y)))
	sc.fit(X)
	Y_ = sc.labels_
	print('spectral clustering :', nmi_eval(Y,Y_))

def test_WardHierarchicalClustering(X,Y):
	from sklearn.cluster import AgglomerativeClustering
	ward = AgglomerativeClustering(n_clusters=len(set(Y)), linkage='ward')
	ward.fit(X)
	Y_ = ward.labels_
	print('ward hierarchical clustering :', nmi_eval(Y,Y_))

def test_AgglomerativeClustering(X,Y):
	from sklearn.cluster import AgglomerativeClustering
	model = AgglomerativeClustering(n_clusters=len(set(Y)))
	model.fit(X)
	Y_ = model.labels_
	print('agglomerative clustering :', nmi_eval(Y,Y_))

def test_DBSCAN(X,Y):
	from sklearn.cluster import DBSCAN
	db = DBSCAN().fit(X)
	Y_ = db.labels_
	# print(Y_)
	print('DBSCAN :', nmi_eval(Y,Y_))

def test_GaussianMixture(X,Y):
	from sklearn import mixture
	clf = mixture.GaussianMixture(n_components=len(set(Y)), covariance_type='full')
	clf.fit(X)
	Y_ = clf.predict(X)
	print('gaussian mixture :', nmi_eval(Y,Y_))

def main():
	X, Y = read('Homework5Tweets.txt')
	# X = X[:500]
	# Y = Y[:500]
	X = feature_extract(X)
	# test_KMeans(X,Y)
	# test_AffinityPropagation(X,Y)
	# test_MeanShift(X,Y)
	
	test_SpectralClustering(X,Y)

	# test_WardHierarchicalClustering(X,Y)
	# test_AgglomerativeClustering(X,Y)
	
	# test_DBSCAN(X,Y)
	# test_GaussianMixture(X,Y)

if __name__ == '__main__':
	main()
