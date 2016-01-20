#Program name : bagofwords.py
#Author       : LAM Wai Man
#Student ID   : 07010702
#Description  : To extract a list of all the word appeared in the reviews. Saved in a dictionary with their corresponding frequency.
#Input        : all the text file in "../raw_byhotel" location
#Output       : bag.dat dump in "../classification"
#Usage        : $python bagofwords.py


import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.probability import FreqDist 
from operator import itemgetter
import pickle

corpus_root = '../raw_byhotel' 
wordlists = PlaintextCorpusReader(corpus_root, '.*.txt')


f=open('stoplist.txt', 'r')
stoplist=[]
ban='IV'
while(ban!=''):
 ban=f.readline()
 ban=ban.strip()
 stoplist.append(ban)

f.close()
banset = set(stoplist)

count = 0
for hotel in wordlists.fileids():
 print hotel
 list1 = wordlists.words(hotel)
 list2 = []
 for w in list1:
  list2.append(w)
 list3 = [w.strip() for w in list2]

 if(count==0):
  fdict = FreqDist(list3)
 else:
  fdict.update(list3)

 count+=1
 print len(fdict)

fdict2=fdict.copy()

for w in fdict.keys()[:]:
 if w.strip() in banset or len(w.strip()) < 3 or len(w.strip()) > 25:
  del fdict2[w]
 elif isinstance(w, unicode):
  del fdict2[w]

for w in fdict2.keys():
 if len(w) < 3:
  print w, len(w)
#print sorted(fdict.keys())

print len(fdict2)
print "Exporting the dictionary..."
fout = open("../classification/bag.dat", "wb")
pickle.dump(fdict2, fout, protocol=0)
fout.close()




print "finish"
