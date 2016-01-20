#Program name : average.py
#Author       : LAM Wai Man
#Student ID   : 07010702
#Description  : To calculate the average score given by all reviews.
#Input        : name.txt, a list of hotel name as table name reference.
#Output       : screen output
#Usage        : $python average.py


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
total = 0
counter = 0
while (name!=''):
  name = f1.readline()
  if(name==''):
    break
  name = name.strip()
  print name
  where = " where location>=5"
  command = 'select count(*) from ' + name + where + ';' 
  con.execute(command) 
  for i in con:
    print i[0]
    counter+=int(i[0]) 
    print counter
print counter

print "Finish\n"
