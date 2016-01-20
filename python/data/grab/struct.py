import psyco
import sys
psyco.full()

from BeautifulSoup import BeautifulSoup,SoupStrainer
import re
import os
import os.path
import urllib2
import urllib
import exceptions
import MySQLdb
import MySQLdb.cursors
from MySQLdb.constants import FIELD_TYPE
import _mysql



infile='url.txt' 
f1=open(infile, 'r')
flag=1
my_conv = { FIELD_TYPE.LONG: int }
db =MySQLdb.connect(host="localhost",user="raymond", passwd="123456",db="dmdata",conv=my_conv, cursorclass=MySQLdb.cursors.Cursor)

con=db.cursor()


url = "IV"
while (url!=''):
  url = f1.readline()
  if(url==''):
    break
  
  i=url.find('-',0)
  i=url.find('-',i+1)
  i=url.find('-',i+1)
  i=url.find('-',i+1)
  start=i+1
  i=url.find('-',i+1)
  end=i
  filename=url[start:end] 
 
  try:
    print "Opening..." + url
    file = urllib.urlopen(url)
    flag = 1
  except IOError, e:
    print e
    continue
  review_no = 0

  while(flag==1):

    

    soup = BeautifulSoup(file)
    
    f=open('struct.txt','w')
    f.write( str(soup.prettify()) ) 
    f.close()
    break
  break
  url=''
f1.close()

print "Finish\n"
