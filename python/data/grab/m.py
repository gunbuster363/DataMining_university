#Program name : m.py
#Author       : LAM Wai Man
#Student ID   : 07010702
#Description  : A prototype for grabbing review from tripadvisor.com. This prototype only grab the review part. 
#Input        : url.txt
#Output       : [hotel name].txt
#Usage        : $python m.py


import psyco
psyco.full()

from BeautifulSoup import BeautifulSoup,SoupStrainer
import re
import os
import os.path
import urllib
import exceptions


infile='url.txt' 
linkto_p = SoupStrainer('p')
linkto_a = SoupStrainer('a')

f2=open(infile, 'r')

flag=1

url = "IV"
while (url!=''):
  url = f2.readline()
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
  if os.path.isfile(filename+'.txt'):
    os.remove(filename+'.txt')
  f=open(filename+'.txt', 'a')
 
  try:
    print "Opening..." + url
    file = urllib.urlopen(url)
    flag = 1
  except IOError, e:
    print e
    continue

  while(flag==1):

    soup = BeautifulSoup(file)
 

    tag=soup.find('p',id=re.compile("^review"))
    print tag 

    tag=soup.find('img', src="http://cdn.tripadvisor.com/img2/sprites/ratings-v6.png")
    print tag['alt']

    tag=soup.find('p',id=re.compile("^review"))
    print tag


    link = soup.find('a', attrs={'class' : re.compile("^util2$")})
    if(soup.find('a', attrs={'class' : re.compile("^util2$")})==None):
      flag=0
    else:
      while True:
        try:
          print "Opening..." + 'http://www.tripadvisor.com' + link['href']
          file = urllib.urlopen('http://www.tripadvisor.com' + link['href'])
          break
        except IOError, e:
          print e
    
  f.close()
f2.close()

print "Finish\n"
