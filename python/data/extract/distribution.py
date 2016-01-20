#Program name : distribution.py
#Author       : LAM Wai Man
#Student ID   : 07010702
#Description  : To get a number of reviews and their label in order to see the distribution of each class label.
#Input        : name.txt, a list of hotel name as table name reference.
#Output       : None
#Usage        : $python distribution.py

#Ref: This prototype will generate a list of unbalanced number of each type of label.

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
outfile='reviewclass.txt' 
f1=open(infile, 'r')
documents = []

my_conv = { FIELD_TYPE.LONG: int }
db =MySQLdb.connect(host="localhost",user="raymond", passwd="123456",db="dmdata",conv=my_conv, cursorclass=MySQLdb.cursors.Cursor)

con=db.cursor()
name = 'IV'



fin=open("btagger.dat", "rb")
tagger = pickle.load(fin)
fin.close()

f2=open("document_lem.txt","a")
f3=open("pos.txt", "a")

while (name!=''):
  name = f1.readline()
  if(name==''):
    break
  name = name.strip()
  print name
  where = ""
  command = 'select review from ' + name + where + ';' 
  con.execute(command) 
  for i in con:
    str = i[0]
    tokens = nltk.word_tokenize(str)
    taglist = tagger.tag(tokens)   
 
    f2.write(str+'\r\n\r\n')
    for w in taglist:
     f3.write(w[1])
    #tuple=(tokens,i[1])
    
    #documents.append(tuple)

#to plot a graph of the distribution of each class label
f1.close()
f2.close()
f3.close()
print "Finish\n"
