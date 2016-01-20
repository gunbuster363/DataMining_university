#Program name : naive_exp.py
#Author       : LAM Wai Man
#Student ID   : 07010702
#Description  : To build a naive bayes classifier and test with 5-folder cross validation. Expression model.
#Input        : location.dat, ../exp.dat
#Output       : features.dat
#Usage        : $python naive_exp.py

import psyco
from psyco.classes import *
psyco.full()

from nltk.corpus import movie_reviews
import random
import nltk
import pickle
import numpy
import re
from operator import itemgetter

def find_chunk(str1,tag):
 cp = nltk.RegexpParser(str1)
 tree = cp.parse(tag)
 list=[]
 for subtree in tree.subtrees():
  if subtree.node == 'CHUNK':
    temp = []
    temp2 = []
    for leaf in subtree:
     if(leaf[1]!='RB'):
      temp.append(leaf[0])
     temp2.append(leaf[0])
    str = ' '.join(temp)
    str2 = ' '.join(temp2)
    list.append(str)
    list.append(str2)
    list += temp
 return list


def find_chunk2(str1,tag):
 cp = nltk.RegexpParser(str1)
 tree = cp.parse(tag)
 list=[]
 for subtree in tree.subtrees():
  if subtree.node == 'CHUNK':
    temp = []
    #print [leaf[0] for leaf in subtree]
    for leaf in subtree:
     if('JJ' in leaf[1]):
      temp.append(leaf[0])
    for leaf in subtree:
     if('NN' in leaf[1]):
      temp.append(leaf[0])
    str = ' '.join(temp)
    list.append(str)
    list += temp
 return list


def find_chunk3(str1,tag):
 cp = nltk.RegexpParser(str1)
 tree = cp.parse(tag)
 list=[]
 for subtree in tree.subtrees():
  if subtree.node == 'CHUNK':
    temp = []
    for leaf in subtree:
      temp.append(leaf[0])
    temp2=[]
    temp2.append(temp[len(temp)-2])
    str = ' '.join(temp2)
    list.append(str)
    list += temp2
 return list

def sort_dict2list(d):
	items = [(v, k) for k, v in d.items()]
	items.sort()
	items.reverse()
	items = [(k, v) for v, k in items]
	list = [w[0] for w in items]
	return list

def document_features(tag):
    d1 = set([w[0] for w in tag])
    list1 = find_chunk('CHUNK: {<JJ.*> <RB>* <NN.*>+}',tag)
    list2 = find_chunk2('CHUNK: {<NN.*>+ <VB.*> <RB>* <JJ.*>}',tag)
    list3 = find_chunk3('CHUNK: {<VB.*> <RB>* <JJ.*> <NN.*>}',tag)
    list1 = list1 + list2 + list3
    document_words = d1.union(set(list1))
    #print list1
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

def k_fold_cross_validation(X, K, randomise = False):
	"""
	Generates K (training, validation) pairs from the items in X.

	Each pair is a partition of X, where validation is an iterable
	of length len(X)/K. So each training iterable is of length (K-1)*len(X)/K.

	If randomise is true, a copy of X is shuffled before partitioning,
	otherwise its order is preserved in training and validation.
	"""
	if randomise: from random import shuffle; X=list(X); shuffle(X)
	for k in xrange(K):
		training = [x for i, x in enumerate(X) if i % K != k]
		validation = [x for i, x in enumerate(X) if i % K == k]
		yield training, validation

tag=[]
#class label
fin = open("location.dat", "rb")
documents = pickle.load(fin)
fin.close()

#word frequency dictionary
fin = open("../exp.dat", "rb")
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

accuracy=0
for train_set, test_set in k_fold_cross_validation(featuresets, K=5):
 print "training classifier..."
 classifier = nltk.NaiveBayesClassifier.train(train_set)

 print "testing classifier..."
 print "Accuracy:",nltk.classify.accuracy(classifier, test_set)
 accuracy+= nltk.classify.accuracy(classifier, test_set)

print "Accuracy using 5-fold validation:", accuracy/5

dict1 =  classifier.show_most_informative_features(n=1000)

fout = open("./features.dat", "wb")
# default protocol is zero
# -1 gives highest prototcol and smallest data file size
pickle.dump(dict1, fout, protocol=0)
fout.close()

