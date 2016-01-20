#Program name : naive_bag.py
#Author       : LAM Wai Man
#Student ID   : 07010702
#Description  : To build a naive bayes classifier and test with 5-folder cross validation.
#Input        : cleanliness.dat, ../bag.dat
#Output       : features.dat
#Usage        : $python naive_bag.py


import psyco
from psyco.classes import *
psyco.full()

from nltk.corpus import movie_reviews
import random
import nltk
import pickle
import numpy
from operator import itemgetter

#return a list of word with descending frequency
def sort_dict2list(d):
	items = [(v, k) for k, v in d.items()]
	items.sort()
	items.reverse()
	items = [(k, v) for v, k in items]
	list = [w[0] for w in items]
	return list

def document_features(document):
    document_words = set(w[0] for w in document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

#class label
fin = open("cleanliness.dat", "rb")
documents = pickle.load(fin)
fin.close()

#word frequency dictionary
fin = open("../bag.dat", "rb")
dict = pickle.load(fin)
fin.close()



print "document length:"
print len(documents)

wordlist = sort_dict2list(dict)

random.shuffle(documents)

word_features = wordlist[:500]

print "features length:"
print len(word_features)


featuresets = [(document_features(d), c) for (d,c) in documents]
train_set, test_set = featuresets[:1400], featuresets[1401:]

print "training..."
classifier = nltk.NaiveBayesClassifier.train(train_set)

print "testing..."
print nltk.classify.accuracy(classifier, test_set)

dict1 =  classifier.show_most_informative_features(n=1000)

fout = open("./features.dat", "wb")
# default protocol is zero
# -1 gives highest prototcol and smallest data file size
pickle.dump(dict1, fout, protocol=0)
fout.close()

