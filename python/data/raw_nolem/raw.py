#Program name : raw.py
#Author       : LAM Wai Man
#Student ID   : 07010702
#Description  : Extract review from the local database for future process.
#Input        : name.txt, a list of hotel name as table name reference.
#Output       : [hotel name].txt
#Usage        : $python raw.py


import psyco
import sys
psyco.full()
import pickle
from BeautifulSoup import BeautifulSoup,SoupStrainer
import re
import os
import os.path
import urllib2
import exceptions
import MySQLdb
import MySQLdb.cursors
from MySQLdb.constants import FIELD_TYPE
import _mysql
import nltk
import re
import nltk.corpus.reader.wordnet

infile='name.txt' 
f1=open(infile, 'r')
my_conv = { FIELD_TYPE.LONG: int }
db =MySQLdb.connect(host="localhost",user="raymond", passwd="123456",db="dmdata",conv=my_conv, cursorclass=MySQLdb.cursors.Cursor)

con=db.cursor()

re_dot = re.compile('.+')
re_at  = re.compile('&quot')
re_amp = re.compile('&amp')
re_f   = re.compile('[;:@#$%^&-]')
re_no  = re.compile('[0-9]+')



name = "IV"
while (name!=''):
  name = f1.readline()
  if(name==''):
    break
  name = name.strip()
  print "Preprocessing...", name
  f2 = open(name+'.txt', 'w')
  command = 'select review from ' + name + ';' 
  con.execute(command) 
  for i in con:
    for j in i:
     str = j
     tokens = nltk.word_tokenize(str)
     j=0
     for w in tokens:
      tokens[j]=tokens[j].replace('/',' ')
      if(tokens[j][len(tokens[j])-1]=='.' and tokens[j][len(tokens[j])-2]!='.'):
       tokens[j]=tokens[j].replace('.', ' .')
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
     str2=' '.join(tokens)
     f2.write(str2+'\n\n') 
  f2.close()
f1.close()

print "Finish\n"
