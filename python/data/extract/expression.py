#Program name : expression.py
#Author       : LAM Wai Man
#Student ID   : 07010702
#Description  : To extract a list of all the word appeared in the reviews. Saved in a dictionary with their corresponding frequency.
#               
#               It also capture phrases by NLTK package, phrase can be in different form such as:
#                1)Adjective + Noun         e.g: good hotel
#                2)Noun + Verb + Adjective  e.g: view is good
#                3)Verb + Adjective + Noun  e.g: is good hotel
#Input        : all the text file in "../raw_byhotel" location
#Output       : exp.dat dump in "../classification"
#Usage        : $python expression.py


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


def find_chunk2(str1):
 cp = nltk.RegexpParser(str1)
 tree = cp.parse(taglist)
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


def find_chunk3(str1):
 cp = nltk.RegexpParser(str1)
 tree = cp.parse(taglist)
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


corpus_root = '../raw_byhotel' 
wordlists = PlaintextCorpusReader(corpus_root, '.*.txt')
wnl = nltk.WordNetLemmatizer()

fin = open("btagger.dat", "rb")
tagger = pickle.load(fin)
fin.close()


count=0
for hotel in wordlists.fileids():
 list4 = []
 print hotel
 taglist = tagger.tag(wordlists.words(hotel))
 #taglist = tagger.tag(wordlists.words(hotel))

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
 stoplist.append(ban.strip())

f.close()
banset = set(stoplist)

fdict2=fdict.copy()

for w in fdict.keys()[:]:
 if w.strip() in banset or len(w.strip()) < 3 :
  del fdict2[w]
 elif isinstance(w, unicode):
  del fdict2[w]



print 'Size of dictionary',len(fdict2)
print 'Exporting the dictionary...'

fout = open("../classification/exp.dat", "wb")
pickle.dump(fdict2, fout, protocol=0)
fout.close()

print "finish"
