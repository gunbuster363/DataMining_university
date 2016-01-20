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



infile='name.txt' 
f1=open(infile, 'r')
my_conv = { FIELD_TYPE.LONG: int }
db =MySQLdb.connect(host="localhost",user="raymond", passwd="123456",db="dmdata",conv=my_conv, cursorclass=MySQLdb.cursors.Cursor)

con=db.cursor()


name = "IV"
while (name!=''):
  id=0
  name = f1.readline()
  if(name==''):
    break
  name = name.strip()
  print name
  command = 'select review from ' + name + ';' 
  con.execute(command) 
  for i in con:
    for j in i:

      f2 = open(name+'_'+str(id)+'.txt', 'w')
      f2.write(j+'\n\n') 
      f2.close()
      id+=1
f1.close()

print "Finish\n"
