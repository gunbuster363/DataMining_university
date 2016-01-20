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
    for i in range(0, len(tagged)-2):
     for w in dict1:
      if tagged[i][0] in dict1[w]:
       temp=dict2[w]
       if 'JJ' in tagged[i][1] and 'NN' in tagged[i+1][1] and len(tagged[i+1][0])>2:
        word = str(tagged[i][0]) + ' ' + str(tagged[i+1][0])
        temp.append(word)
       elif 'NN' in tagged[i][1] and i!=0 and 'JJ' in tagged[i-1][1]:
        word = str(tagged[i-1][0]) + ' ' + str(tagged[i][0])
        temp.append(word)
       dict2[w]=temp

#class label
fin = open("triptype.dat", "rb")
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




