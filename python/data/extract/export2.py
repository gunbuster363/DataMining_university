#Program name : export2.py
#Author       : LAM Wai Man
#Student ID   : 07010702
#Description  : To extract a list the tags of all the words appeared in the reviews.
#Input        : all the text file in "../raw_byhotel" location
#Output       : pos.txt
#Usage        : $python export2.py


import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.probability import FreqDist 
from operator import itemgetter
import pickle


corpus_root = '../raw_byhotel' 
wordlists = PlaintextCorpusReader(corpus_root, '.*.txt')

fin = open("btagger.dat", "rb")
tagger = pickle.load(fin)
fin.close()

f2=open("document_lem.txt","a")
f3=open("pos.txt","a")


count=0
for hotel in wordlists.fileids():
 list4 = []
 print hotel
 taglist = tagger.tag(wordlists.words(hotel))
 str1=' '.join(wordlists.words(hotel))
 f2.write(str1+'\r\n\r\n')
 for w in taglist:
  f3.write(str(w[1])+' ')
 f3.write('\r\n\r\n')

print "finish"
