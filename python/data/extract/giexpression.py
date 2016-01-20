#Program name : wordlist.py
#Author       : LAM Wai Man
#Student ID   : 07010702
#Description  : To extract a list of all the word appeared in the reviews. Saved in a dictionary with their corresponding frequency.
#               All the words are lemmatized and stemmed in order to increase the accuracy.
#               It also capture phrases by NLTK package, phrase can be in different form such as:
#                1)Adjective + Noun         e.g: good hotel
#                2)Noun + Verb + Adjective  e.g: view is good
#                3)Verb + Adjective + Noun  e.g: is good hotel
#Input        : all the text file in "../raw" location
#Output       : dict.dat dump in "../classification"
#Usage        : $python wordlist.py

import psyco 
from psyco.classes import *
psyco.full()
import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.probability import FreqDist 
from operator import itemgetter
import pickle

def find_chunk(str1):
 cp = nltk.RegexpParser(str1)
 tree = cp.parse(taglist)
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
    list.append(str)
    list += temp

 return list


def find_chunk2(str1):
 cp = nltk.RegexpParser(str1)
 tree = cp.parse(taglist)
 list=[]
 for subtree in tree.subtrees():
  if subtree.node == 'CHUNK':
    temp = []
    #print [leaf[0] for leaf in subtree]
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
    list.append(str)
    #print str
    list += temp2

 return list


def find_chunk3(str1):
 cp = nltk.RegexpParser(str1)
 tree = cp.parse(taglist)
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
    list.append(str)
    list += temp2

 return list


corpus_root = '../raw_byhotel' 
wordlists = PlaintextCorpusReader(corpus_root, '.*.txt')

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

count = 0
for hotel in wordlists.fileids():

 list4 = []
 print hotel
 taglist = nltk.pos_tag(wordlists.words(hotel))
 #print taglist
 list1 = find_chunk('CHUNK: {<JJ.*> <RB>* <NN.*>+}')
 list2 = find_chunk2('CHUNK: {<NN.*>+ <VB.*> <RB>* <JJ.*>}')
 list3 = find_chunk3('CHUNK: {<VB.*> <RB>* <JJ.*> <NN.*>}')

 list4 = list1 + list2 + list3

 if(count==0):
  fdict = FreqDist(list4)
 else:
  fdict.update(list4)

 count+=1
 print 'Size of dictionary:',len(fdict)
 print ''


f=open('stoplist.txt', 'r')
stoplist=[]
ban='IV'
while(ban!=''):
 ban=f.readline()
 ban=ban.strip()
 stoplist.append(ban)

f.close()
banset = set(stoplist)

fdict2=fdict.copy()

for w in fdict.keys()[:]:
 if w.strip() in banset or len(w.strip()) < 3 :
  del fdict2[w]
 elif isinstance(w, unicode):
  del fdict2[w]



print len(fdict2)
fout = open("../classification/ctriptype/giexp.dat", "wb")
# default protocol is zero
# -1 gives highest prototcol and smallest data file size
pickle.dump(fdict2, fout, protocol=2)
fout.close()

print "finish"
