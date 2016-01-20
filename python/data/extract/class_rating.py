#Program name : class_rating.py
#Author       : LAM Wai Man
#Student ID   : 07010702
#Description  : To extract a list of reviews and their correspinding label for training of classifier.
#               The labels would be : positive, negative
#Input        : name.txt
#Output       : goodbad.dat dump in "../classification/rating" location
#Usage        : $python class_rating.py



import psyco
from psyco.classes import *
psyco.full()

import sys
import nltk
from nltk.probability import FreqDist

import re
import os
import os.path
import exceptions
import MySQLdb
import MySQLdb.cursors
from MySQLdb.constants import FIELD_TYPE
import _mysql
import pickle


infile='name.txt'
f1=open(infile, 'r')
documents = []

my_conv = { FIELD_TYPE.LONG: int }
db =MySQLdb.connect(host="localhost",user="raymond", passwd="123456",db="dmdata",conv=my_conv, cursorclass=MySQLdb.cursors.Cursor)

con=db.cursor()

re_dot = re.compile('.+')
re_at  = re.compile('&quot')
re_amp = re.compile('&amp')
re_f   = re.compile('[;:@#$%^&-]')
re_no  = re.compile('[0-9]+')

wcr = nltk.corpus.reader.wordnet.WordNetCorpusReader('/usr/share/nltk_data/corpora/wordnet')

fin = open("btagger.dat", "rb")
tagger = pickle.load(fin)
fin.close()


name = 'IV'

pos=0
neg=0

while (neg < 1000 or pos < 1000 ):
  name = f1.readline()
  if(name==''):
    break
  name = name.strip()
  print name
  where = ""#"\nwhere rating!=\'NULL\'"
  command = 'select review, rating from ' + name + where + ';' 
  con.execute(command) 
  for i in con:
    str = i[0]
    tokens = nltk.word_tokenize(str)
    j=0
    for w in tokens:
     tokens[j] = w.lower()
     tokens[j]=tokens[j].replace('/',' ')
     if(tokens[j][len(tokens[j])-1]=='.' and tokens[j][len(tokens[j])-2]!='.'):
      tokens[j]=tokens[j].replace('.', '')
     elif(re_dot.search(tokens[j])):
      if(len(tokens[j])>1):
       tokens[j]=tokens[j].replace('.', ' ')
     if(re_at.search(tokens[j])):
      tokens[j]=tokens[j].replace('&quot',' ')
     if(re_amp.search(tokens[j])):
      tokens[j]=tokens[j].replace('&amp',' ')
     if(re_f.search(tokens[j])):
      tokens[j]=tokens[j].replace(';',' ')
      tokens[j]=tokens[j].replace(':',' ')
      tokens[j]=tokens[j].replace('@',' ')
      tokens[j]=tokens[j].replace('#',' ')
      tokens[j]=tokens[j].replace('$',' ')
      tokens[j]=tokens[j].replace('%',' ')
      tokens[j]=tokens[j].replace('^',' ')
      tokens[j]=tokens[j].replace('&',' ')
      tokens[j]=tokens[j].replace('-',' ')
     if(re_no.search(tokens[j])):
      tokens[j]=' '
     tokens[j] = tokens[j].lower()
     j=j+1    

    taglist = tagger.tag(tokens)
    tokens2 = []
    for k in range(0, len(taglist)-1):
     if 'ADJ' in taglist[k][1]:
      t=wcr.morphy(taglist[k][0],'a')
      if not t:
       tokens2.append(taglist[k][0])
      else:
       tokens2.append(t)
     elif 'VB' in taglist[k][1]:
      t=wcr.morphy(taglist[k][0],'v')
      if not t:
       tokens2.append(taglist[k][0])
      else:
       tokens2.append(t)
     elif 'NN' in taglist[k][1]:
      t=wcr.morphy(taglist[k][0],'n')
      if not t:
       tokens2.append(taglist[k][0])
      else:
       tokens2.append(t)
     else:
      tokens2.append(taglist[k][0])
    
    tokens = tagger.tag(tokens2)   
    if(len(tokens)==0):
     print "empty text found after preprocessing...discard"
     continue
    if(i[1]>3 and pos<1000):
     tuple = (tokens,"positive")
     documents.append(tuple)
     pos+=1

    if(i[1]<3 and neg<1000):
     tuple = (tokens,"negative")
     documents.append(tuple)
     neg+=1

list=[]
for w in documents:
 list.append(w[1])
print len(documents)
dict=FreqDist(list)
dict.tabulate()
for w in dict:
 print w, dict[w]
f1.close()
fout = open("../classification/rating/goodbad.dat", "wb")
pickle.dump(documents, fout, protocol=0)
fout.close()
print "Finish\n"
