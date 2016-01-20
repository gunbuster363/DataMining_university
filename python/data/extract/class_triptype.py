#Program name : class_triptype.py
#Author       : LAM Wai Man
#Student ID   : 07010702
#Description  : To extract a list of reviews and their correspinding label for training of classifier.
#               The labels would be : Family, Business, Couples, Solo traveler, Friends Getaway
#Input        : name.txt
#Output       : triptype.dat dump in "../classification/triptype" location
#Usage        : $python class_triptype.py




import psyco
import sys
import nltk
from nltk.probability import FreqDist
psyco.full()

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

cou=0
fam=0
bus=0
sol=0
fri=0

while (cou < 500 or fam < 500 or bus < 500 or sol < 500 or fri < 500):
  name = f1.readline()
  if(name==''):
    break
  name = name.strip()
  print name
  where = "\nwhere triptype=\'Couples\' OR triptype=\'Family\' OR triptype=\'Business\' OR triptype=\'Solo travel\' OR triptype=\'Friends getaway\'"
  command = 'select review,triptype from ' + name + where + ';' 
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
     j+=1

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
    tokens=tagger.tag(tokens2)
    tuple=(tokens,i[1])

    if(len(tokens)==0):
     print "empty text found after preprocessing...discard"
     continue 

    
    if('Couples' in i[1] and cou<500):
     documents.append(tuple)
     cou+=1

    if('Family' in i[1] and fam<500):
     documents.append(tuple)
     fam+=1
    if('Business' in i[1] and bus<500):
     documents.append(tuple)
     bus+=1

    if('Solo' in i[1] and sol<500):
     documents.append(tuple)
     sol+=1
    if('Friends' in i[1] and fri<500):
     documents.append(tuple)
     fri+=1



list=[]
for w in documents:
 list.append(w[1])
print len(documents)
dict=FreqDist(list)
dict.tabulate()
for w in dict:
 print w, dict[w]
f1.close()
fout = open("../classification/triptype/triptype.dat", "wb")
pickle.dump(documents, fout, protocol=0)
fout.close()
print "Finish\n"
