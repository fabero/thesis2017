# review_classifier.py
# By Lennart Faber
# run: 'python3 review_classifier.py trainfile testfile'
import sys
import numpy as np
import json

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn import metrics
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.svm import LinearSVC
from nltk.corpus import stopwords
from nltk.stem.snowball import *

# words could be stemmed, but did not improve performance
#stemmer  = DutchStemmer()
#analyzer = CountVectorizer().build_analyzer()

# as found on 'http://stackoverflow.com/questions/11116697/how-to-get-most-informative-features-for-scikit-learn-classifiers'
def show_most_important_features(vectorizer, clf, n=20):
	feature_names = vectorizer.get_feature_names()
	coefs_with_nfs = sorted(zip(clf.coef_[0], feature_names))
	top = zip(coefs_with_nfs[:n], coefs_with_nfs[:-(n+1):-1])
	for (coef_1,fn_1), (coef_2, fn_2) in top:
		print("\t%.4f\t%-15s\t\t%.4f\t%-15s"% (coef_1, fn_1, coef_2, fn_2))

# calculates accuracy
def accuracy(y_true, y_predicted):
	correct, total = 0, 0.0
	for gold, pred in zip(y_true, y_predicted):
		if gold==pred:
			correct+=1
		total +=1
	print(correct/total)

# prints accuracy and f scores for the all-five baseline and the classifier
def results(y_test, y_predicted, allfive_predicted, test_reviews):
	print("\n###### RESULTS: ######")
	print("Accuracy of all-five baseline:")
	accuracy(y_test, allfive_predicted)

	print("Accuracy of this classifier:")
	accuracy(y_test, y_predicted)

	print()
	print("F-scores for all-five classifier:")
	print(metrics.classification_report(y_test, allfive_predicted, target_names = test_reviews['target_names']))

	print("F-scores for this classifier:")
	print(metrics.classification_report(y_test, y_predicted, target_names = test_reviews['target_names']))

def stemmed_words(doc):
    return (stemmer.stem(w) for w in analyzer(doc))

def main(argv):
	# load files
	train_file = sys.argv[1]
	test_file = sys.argv[2]

	with open(train_file, 'r') as fp:
		train_reviews = json.load(fp)
	with open(test_file, 'r') as fp:
		test_reviews = json.load(fp)

	#convert lists to arrays
	train_reviews['target'] = np.asarray(train_reviews['target'])
	train_reviews['data'] = np.asarray(train_reviews['data'])
	
	test_reviews['target'] = np.asarray(test_reviews['target'])
	test_reviews['data'] = np.asarray(test_reviews['data'])

	# print stats
	print("#inst train: %s" % len(train_reviews['target']))
	print("#inst test: %s" % len(test_reviews['target']))

	print("training model...")
	# parameters will be adapted to turn on/of binary mode and change ngram range
	count_vectorizer_binary = CountVectorizer(ngram_range=(1,3)).fit(train_reviews['data'])
	x_train = count_vectorizer_binary.transform(train_reviews['data'])

	clf = LinearSVC()
	clf.fit(x_train, train_reviews['target'])

	x_test = count_vectorizer_binary.transform(test_reviews['data'])
	y_predicted = clf.predict(x_test)

	# test against the case of simply always predicting a 5-star rating
	allfive_predicted = [4 for review in test_reviews['target']]

	results(test_reviews['target'], y_predicted, allfive_predicted, test_reviews)

	print("Most informative features: ")
	show_most_important_features(count_vectorizer_binary, clf)


if __name__=='__main__':
	main(sys.argv)