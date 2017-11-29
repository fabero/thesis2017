# database_builder.py
# used to construct useful databases from raw data
# by Lennart Faber
# 17-11-17

import sys
import numpy as np
import json

def main(argv):
	filename = sys.argv[1]
	retailer = sys.argv[2]

	database = {}
	database['target_names'] = ["1","2","3","4","5"]
	database['data'] = []
	database['target'] = []

	counts = {1:0, 2:0, 3:0, 4:0, 5:0}
	with open(filename, 'r') as f:
		# Extract text and ratings from the file and add them to the dictionary
		for line in f:
			review = eval(line)
			if(retailer == "bol"):
				review_text = review['reviewText']
				review_rating = int(review['rating'])
			else:
				review_text = review['text']
				review_rating = round(eval(review['rating'].replace(',','.'))/2)
				if (review_rating == 0):
					review_rating = 1

			database['data'].append(review_text)
			database['target'].append(database['target_names'].index(str(int(review_rating))))

	#convert lists to arrays for efficiency
	database['target'] = np.asarray(database['target'])
	database['data'] = np.asarray(database['data'])

	 # generate random list of indices
	indices = np.random.permutation(len(database['data']))
	len_devtest = int(len(database['data'])*0.2)		   
	len_test = int(len(database['data'])*0.1)              

	#converting the arrays back to lists, to allow for json writing

	#complete set
	x_complete = database['data'].tolist()
	y_complete = database['target'].tolist()
	# train part
	x_train = database['data'][indices[:-len_devtest]].tolist()
	y_train = database['target'][indices[:-len_devtest]].tolist()

	# devtest part
	x_devtest = database['data'][indices[-len_devtest:-len_test]].tolist()
	y_devtest = database['target'][indices[-len_devtest:-len_test]].tolist()

	# test part
	x_test = database['data'][indices[-len_test:]].tolist()
	y_test = database['target'][indices[-len_test:]].tolist()

	print("Total: ", len(x_complete))
	print("Train: ", len(x_train))
	print("Dev: ", len(x_devtest))
	print("Test: ", len(x_test))

	complete_db = {'target_names' : ["1","2","3","4","5"], 'data' : x_complete, 'target' : y_complete}
	train_db = {'target_names' : ["1","2","3","4","5"], 'data' : x_train, 'target' : y_train}
	devtest_db = {'target_names' : ["1","2","3","4","5"], 'data' : x_devtest, 'target' : y_devtest}
	test_db = {'target_names' : ["1","2","3","4","5"], 'data' : x_test, 'target' : y_test}

	print("dumping databases to files...")
	# Dump dictionaries to json file
	if(retailer == 'bol'):
		with open('bol_train.json','w') as fp:
			json.dump(train_db, fp)
		with open('bol_devtest.json', 'w') as fp:
			json.dump(devtest_db, fp)
		with open('bol_test.json', 'w') as fp:
			json.dump(test_db, fp)
		with open('bol_complete.json', 'w') as fp:
			json.dump(complete_db, fp)

	else:
		with open('coolblue_train.json','w') as fp:
			json.dump(train_db, fp)
		with open('coolblue_devtest.json', 'w') as fp:
			json.dump(devtest_db, fp)
		with open('coolblue_test.json', 'w') as fp:
			json.dump(test_db, fp)
		with open('coolblue_complete.json', 'w') as fp:
			json.dump(complete_db, fp)

	print("done.")

if __name__=='__main__':
	main(sys.argv)