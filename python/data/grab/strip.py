#Program name : strip.py
#Author       : LAM Wai Man
#Student ID   : 07010702
#Description  : To remove tables(each table represent a hotel) without content(review)
#Input        : name.txt
#Output       : None
#Usage        : $python strip.py



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

counter = 0

name = "IV"
while (name!=''):
  name = f1.readline()
  if(name==''):
    break
  name = name.strip()
  print name
  
  command = 'select count(*) from ' + name + ';' 
  con.execute(command) 
  for i in con:
    for j in i:
      num = int(j)
      counter = counter +1
      if(num==0):
        print "Dropping table without review..."
        con.execute("drop table "+name+";")
        print con
      else:
        print num
      break
    break 
f1.close()

print counter
print "Finish\n"
