#Program name : retrieve.py
#Author       : LAM Wai Man
#Student ID   : 07010702
#Description  : To retrieve the informative expression
#Input        : features.dat
#Output       : Screen Standard output
#Usage        : $python retrieve.py


import psyco
from psyco.classes import *
psyco.full()
import random
import nltk
import pickle
from operator import itemgetter

#retrieve information from 1 document
def retrieve_features(tagged):
    global dict1
    global dict2
    for w in dict1:
     #what storing in dict1 is some sets
     set1=dict1[w]
     #dict2 now is empty list
     temp2=dict2[w]
     #a empty list
     temp3=list()
     #retrieve any expression
     for w2 in set1:
      if(' ' in w2):
       temp3.append(w2)
     temp2=temp2+temp3
     dict2[w]=temp2

    for i in range(0, len(tagged)-2):
     #for every category
     for w in dict1:
      #if the word is in the most informative feature set
      if tagged[i][0] in dict1[w]:
       #load the set to a temp set, for later adding any new discovered expression
       temp=dict2[w]
       if 'JJ' in tagged[i][1] and 'NN' in tagged[i+1][1] and len(tagged[i+1][0])>2:
        word = str(tagged[i][0]) + ' ' + str(tagged[i+1][0])
        temp.append(word)
       elif 'NN' in tagged[i][1] and i!=0 and 'JJ' in tagged[i-1][1]:
        word = str(tagged[i-1][0]) + ' ' + str(tagged[i][0])
        temp.append(word)
       dict2[w]=temp

#class label
fin = open("goodbad.dat", "rb")
documents = pickle.load(fin)
fin.close()

#interesting feature
fin = open("features.dat", "rb")
dict1 = pickle.load(fin)
fin.close()


dict2=dict1.copy()
for w in dict1:
 dict2[w]=list()

for i in documents:
 retrieve_features(i[0])

for w in dict1:
 temp=dict2[w]
 tset=set(temp)
 dict2[w]=tset
 print w, dict2[w]
 print '\n'




