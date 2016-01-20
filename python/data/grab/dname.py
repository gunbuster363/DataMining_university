#Program name : dname.py
#Author       : LAM Wai Man
#Student ID   : 07010702
#Description  : To extract a list of hotel names from the local mysql database. 
#Input        : tables from the mysql database
#Output       : name.txt
#Usage        : $python dname.py



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



my_conv = { FIELD_TYPE.LONG: int }
db =MySQLdb.connect(host="localhost",user="raymond", passwd="123456",db="dmdata",conv=my_conv, cursorclass=MySQLdb.cursors.Cursor)

con=db.cursor()

f1 = open("name.txt", "w")
command = 'show tables;' 
con.execute(command) 
for i in con:
  for j in i:
    f1.write(j+'\n')

f1.close() 
print "Finish\n"
