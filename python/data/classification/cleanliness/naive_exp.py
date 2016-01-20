#Program name : naive_exp.py
#Author       : LAM Wai Man
#Student ID   : 07010702
#Description  : To build a naive bayes classifier and test with 5-folder cross validation. Expression model.
#Input        : cleanliness.dat, ../exp.dat
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



#return a list of word with descending frequency
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

tag=[]
#class label
fin = open("cleanliness.dat", "rb")
documents = pickle.load(fin)
fin.close()

#word frequency dictionary
fin = open("../exp.dat", "rb")
dict = pickle.load(fin)
fin.close()

vice=[]
v='IV'
f=open('vice.txt', 'r')
while(v!=''):
  v=f.readline()
  v=(v.lower()).strip()
  vice.append(v)
f.close()
viceset=set(vice)

virtue=[]
v1='IV'
f=open('virtue.txt', 'r')
while(v1!=''):
  v1=f.readline()
  v1=(v1.lower()).strip()
  virtue.append(v1)
f.close()
virtueset=set(virtue)

print "document length:"
print len(documents)

wordlist = sort_dict2list(dict)

random.shuffle(documents)

word_features = wordlist[:500]

print "features length:"
print len(word_features)

featuresets = [(document_features(d), c) for (d,c) in documents]
train_set, test_set = featuresets[:2000], featuresets[2000:]

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

