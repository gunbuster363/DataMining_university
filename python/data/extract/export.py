#Program name : export.py
#Author       : LAM Wai Man
#Student ID   : 07010702
#Description  : To create a file containing all the reviews in the local database, for Matlab usage.
#Input        : name.txt, a list of hotel name as table name reference.
#Output       : documents.txt
#Usage        : $python export.py


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
name = 'IV'

li = []
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
    li.append(i[0])

fout = open('documents.txt','a')
for i in li:
 fout.write(i+'\r\n\r\n')
fout.close()
print "Finish\n"
