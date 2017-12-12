# review_analyzer.py
# By Lennart Faber
# run: python3 review_analyzer.py db1 db2

import sys
import json
from collections import defaultdict
import heapq
from nltk.tokenize import word_tokenize

def createindex(db):
	# store counts of tokens in a dict
	token_index = defaultdict(int)
	for review in db:
		tokens = word_tokenize(review)
		for token in tokens:
			token_index[token] += 1
	return(token_index)

def main(argv):
	print("indexing files...")
	with open(sys.argv[1],'r') as fp:
		review_db1 = json.load(fp)['data']
		index1 = createindex(review_db1)
	with open(sys.argv[2],'r') as fp:
		review_db2 = json.load(fp)['data']
		index2 = createindex(review_db2)

	print("indexed files.")
	print("unique tokens in file '{}': {}".format(sys.argv[1],len(index1)))
	print("unique tokens in file '{}': {}".format(sys.argv[2],len(index2)))
	
	most_occurring_tokens = zip(heapq.nlargest(15,index1, key = index1.get),heapq.nlargest(15,index2, key = index2.get))
	print("most occurring tokens:")
	print("{}\t{}".format('first file', 'second file'))
	for word1, word2 in most_occurring_tokens:
		print("{}\t\t{}".format(word1,word2))
	set1 = set(index1) - set(index2)
	set2 = set(index2) - set(index1)
	print("tokens of first file not occurring in second file:")
	print(len(set1))
	print("tokens of second file not occurring in first file:")
	print(len(set2))

	oov1 = len(set2)/len(index2)
	oov2 = len(set1)/len(index1)
	print("oov rate file1:file2: ",oov1)
	print("oov rate file2:file1: ",oov2)

if __name__=='__main__':
	main(sys.argv)

