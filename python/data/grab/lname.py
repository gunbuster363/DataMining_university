#Program name : lname.py
#Author       : LAM Wai Man
#Student ID   : 07010702
#Description  : To extract a list of hotel names within a specific text file storing the hyperlinks of the reviews from tripadvisor.com.
#               For example, given http://www.tripadvisor.com/ShowUserReviews-g294217-d305813-r48911637-Langham_Place_Hong_Kong-Hong_Kong_Hong_Kong_Region.html#REVIEWS, extract Langham_Place_Hong_Kong
#Input        : url.txt
#Output       : name.txt
#Usage        : $python lname.py

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



infile='url.txt' 
f1=open(infile, 'r')
flag=1
my_conv = { FIELD_TYPE.LONG: int }


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

  f2=open('name.txt', 'a')
  f2.write(filename+'\n')
  f2.close()
f1.close()

print "Finish\n"
