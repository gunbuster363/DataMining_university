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

def find_chunk1(str1,tag):
 cp = nltk.RegexpParser(str1)
 tree = cp.parse(tag)
 list=[]
 for subtree in tree.subtrees():
  if subtree.node == 'CHUNK':
    temp = []
    for leaf in subtree:
     if(leaf[1]!='RB' and leaf[1]!='RP'):
      temp.append(leaf[0])
    if(temp[0] in viceset):
     temp[0]='positive'
     #print temp[0]
    elif(temp[0] in virtueset):
     temp[0]='negative'
     #print temp[0]
    str = ' '.join(temp)
    #print str
    list.append(str)
 return list

def find_chunk2(str1,tag):
 cp = nltk.RegexpParser(str1)
 tree = cp.parse(tag)
 list=[]
 for subtree in tree.subtrees():
  if subtree.node == 'CHUNK':
    temp = []
    for leaf in subtree:
     if(leaf[1]!='RB' and leaf[1]!='RP'):
      temp.append(leaf[0])
    temp2=[]
    temp2.append(temp[len(temp)-1])
    temp2.append(temp[0])
    if(temp2[0] in viceset):
     temp2[0]='positive'
     #print temp2[0]
    elif(temp2[0] in virtueset):
     temp2[0]='negative'
     #print temp2[0]
    str = ' '.join(temp2)
    #print str
    list.append(str)
  return list

def find_chunk3(str1,tag):
 cp = nltk.RegexpParser(str1)
 tree = cp.parse(tag)
 list=[]
 for subtree in tree.subtrees():
  if subtree.node == 'CHUNK':
    temp = []
    for leaf in subtree:
     if(leaf[1]!='RB' and leaf[1]!='RP'):
      temp.append(leaf[0])
    temp2=[]
    temp2.append(temp[len(temp)-2])
    temp2.append(temp[len(temp)-1])
    if(temp2[0] in viceset):
     temp2[0]='positive'
     #print temp2[0]
    elif(temp2[0] in virtueset):
     temp2[0]='negative'
     #print temp2[0]
    str = ' '.join(temp2)
    #print str
    list.append(str)
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
    d1 = set(w[0] for w in tag)
    global count
    list1 = find_chunk1('CHUNK: {<JJ.*> <RB>* <NN.*>}', tag)
    list2 = find_chunk2('CHUNK: {<NN.*> <VB.*> <RB>* <JJ.*>}', tag)
    list3 = find_chunk3('CHUNK: {<VB.*> <RB>* <JJ.*> <NN.*>}', tag)
    list1 = list1 + list2 + list3
    document_words = d1.union(set(list1))
    print list1
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    if(count%50==0):
      print count
    count+=1
    return features
tag=[]
count=0
#class label
fin = open("cleanliness.dat", "rb")
documents = pickle.load(fin)
fin.close()

#word frequency dictionary
fin = open("giexp.dat", "rb")
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
print viceset

virtue=[]
v1='IV'
f=open('virtue.txt', 'r')
while(v1!=''):
  v1=f.readline()
  v1=(v1.lower()).strip()
  virtue.append(v1)
f.close()
virtueset=set(virtue)
print virtueset

print "document length:"
print len(documents)

wordlist = sort_dict2list(dict)

random.shuffle(documents)

word_features = wordlist[:2000]

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

