#Program name : dm.py
#Author       : LAM Wai Man
#Student ID   : 07010702
#Description  : To grab reviews from tripadvisor.com. It will grab the review body and associated score attributes.
#Input        : url.txt
#Output       : Store directly into a local mysql database.
#Usage        : $python dm.py



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
    file = urllib2.urlopen(url)
    flag = 1
  except IOError, e:
    print e
    continue
  review_no = 0
  con.execute("create table if not exists " +filename+" (Id INT, review text, triptype TEXT, rating INT, value INT, rooms INT, location INT, cleanliness INT, service INT, Date_Of_Stay TEXT, Visit_Was_For TEXT, Traveled_With TEXT, PRIMARY KEY (Id))")
  result = con.fetchall()
  print result

  while(flag==1):

    

    soup = BeautifulSoup(file)
    tag = soup.findAll(id=re.compile("^UR"))
   
    for i in xrange(0, len(tag)):

      A_triptype    = 0
      A_rating      = 0
      A_review      = 0
      A_value       = 0
      A_rooms       = 0
      A_location    = 0
      A_cleanliness = 0
      A_service     = 0
      A_dos         = 0
      A_vwf         = 0
      A_tw          = 0
      rating        = ' '
      rtype         = ' '
      rvalue        = ' '
      review        = ' '
      triptype      = ' '
      value         = ' '
      rooms         = ' '
      location      = ' '
      cleanliness   = ' '
      service       = ' '
      dos           = ' '
      vwf           = ' ' 
      tw            = ' '
      info_data     = ' '
      info_type     = ' '


      review_no = review_no + 1
      for j in xrange(0, len(tag[i].contents)):
	if not isinstance(tag[i].contents[j], unicode):
          if (tag[i].contents[j].name == "div"): #div tag
            if (tag[i].contents[j]['class']=="wrap forSave"): #wrap for save
              for k in xrange(0, len(tag[i].contents[j].contents)):
                if not isinstance(tag[i].contents[j].contents[k], unicode):
                  if(tag[i].contents[j].contents[k].name=="div"):
                    if(tag[i].contents[j].contents[k]['class']=="profile"): #profile
		      for l in xrange(0, len(tag[i].contents[j].contents[k].contents)):
                        if not isinstance(tag[i].contents[j].contents[k].contents[l], unicode):
                          if(tag[i].contents[j].contents[k].contents[l].name == "div"):
                            if(tag[i].contents[j].contents[k].contents[l]['class'] == "date "):
			      for m in xrange(0, len(tag[i].contents[j].contents[k].contents[l].contents)):
				if not isinstance(tag[i].contents[j].contents[k].contents[l].contents[m], unicode):
 				  if(tag[i].contents[j].contents[k].contents[l].contents[m].name == "span"):
				    if(tag[i].contents[j].contents[k].contents[l].contents[m]['class'] == "triptype"):
				      for n in xrange(0, len(tag[i].contents[j].contents[k].contents[l].contents[m].contents)):
					if isinstance(tag[i].contents[j].contents[k].contents[l].contents[m].contents[n], unicode):
					  triptype = str( tag[i].contents[j].contents[k].contents[l].contents[m].contents[n] )
					  tlist = triptype.split('\n')
					  triptype = tlist[2]
					  A_triptype = 1
			    elif(tag[i].contents[j].contents[k].contents[l]['class'] == "rating"):#total rating, if any
			      for m in xrange(0, len(tag[i].contents[j].contents[k].contents[l].contents)):
                                if not isinstance(tag[i].contents[j].contents[k].contents[l].contents[m], unicode):
                                  if(tag[i].contents[j].contents[k].contents[l].contents[m].name == "span"):	 
				    for n in xrange(0, len(tag[i].contents[j].contents[k].contents[l].contents[m].contents)):
				      if not isinstance(tag[i].contents[j].contents[k].contents[l].contents[m].contents[n], unicode):
					if(tag[i].contents[j].contents[k].contents[l].contents[m].contents[n].name == "img"):
					  str9 = str( tag[i].contents[j].contents[k].contents[l].contents[m].contents[n]['alt'])
					  slist = str9.split(' ')
					  rating = slist[0]
					  A_rating = 1
                            if(A_triptype == 1 & A_rating == 1):
			      break
 
            if (tag[i].contents[j]['class']=="summary"): #summary
              for k in xrange(0, len(tag[i].contents[j].contents)):
                if not isinstance(tag[i].contents[j].contents[k], unicode):
                  if(tag[i].contents[j].contents[k].name == "div"):
                    if(tag[i].contents[j].contents[k]['class']=="entry"):
                      for l in xrange(0, len(tag[i].contents[j].contents[k].contents)):
                        if not isinstance(tag[i].contents[j].contents[k].contents[l], unicode):
                          if(tag[i].contents[j].contents[k].contents[l].name == "p"):
                            for m in xrange(0, len(tag[i].contents[j].contents[k].contents[l].contents)):
                              if isinstance(tag[i].contents[j].contents[k].contents[l].contents[m], unicode):
                                review = str( tag[i].contents[j].contents[k].contents[l].contents[m] )
                                review = review.replace('(', ' ')
                                review = review.replace('\'','\\\'')
                                review = review.replace(')', ' ')
				A_review=1
                                break
	    if (tag[i].contents[j]['class']=="rating-list"): #rating list
              for k in xrange(0, len(tag[i].contents[j].contents)):
                if not isinstance(tag[i].contents[j].contents[k], unicode):
                  if(tag[i].contents[j].contents[k].name == "ul"):
                    for l in xrange(0, len(tag[i].contents[j].contents[k].contents)):
                      if not isinstance(tag[i].contents[j].contents[k].contents[l], unicode):
                        if(tag[i].contents[j].contents[k].contents[l].name == "li"):
                          for m in xrange(0,len(tag[i].contents[j].contents[k].contents[l].contents)):
                            if not isinstance(tag[i].contents[j].contents[k].contents[l].contents[m], unicode): 
                              if(tag[i].contents[j].contents[k].contents[l].contents[m].name == "ul"): #ul
				for n in xrange(0, len(tag[i].contents[j].contents[k].contents[l].contents[m].contents)):
                                  if not isinstance(tag[i].contents[j].contents[k].contents[l].contents[m].contents[n], unicode):
                                    if(tag[i].contents[j].contents[k].contents[l].contents[m].contents[n].name == "li"):
				      for o in xrange(0, len(tag[i].contents[j].contents[k].contents[l].contents[m].contents[n].contents)):
                                        if isinstance(tag[i].contents[j].contents[k].contents[l].contents[m].contents[n].contents[o], unicode):
					  rtype = str( tag[i].contents[j].contents[k].contents[l].contents[m].contents[n].contents[o])# rating type
					  rtype = rtype.replace('\n','')
					  rtype=rtype.lstrip(' ')
					  rtype=rtype.rstrip(' ')

                                        elif (tag[i].contents[j].contents[k].contents[l].contents[m].contents[n].contents[o].name == "span"):
                                          for p in xrange(0, len(tag[i].contents[j].contents[k].contents[l].contents[m].contents[n].contents[o].contents)):
                                            if not isinstance(tag[i].contents[j].contents[k].contents[l].contents[m].contents[n].contents[o].contents[p],unicode):
					      if(tag[i].contents[j].contents[k].contents[l].contents[m].contents[n].contents[o].contents[p].name =="img"):
                                                rating = str(tag[i].contents[j].contents[k].contents[l].contents[m].contents[n].contents[o].contents[p]['alt'])#the value of rating 
						array_rating = rating.split(' ')
						rvalue = array_rating[0]

                                      if(rtype=="Value"):
                                        A_value = 1
                                        value = rvalue
                                      elif(rtype=="Rooms"):
                                        A_rooms = 1
                                        rooms = rvalue
                                      elif(rtype=="Location"):
                                        A_location=1
                                        location = rvalue
                                      elif(rtype=="Cleanliness"):
                                        A_cleanliness = 1
                                        cleanliness = rvalue
                                      elif(rtype=="Service"):
                                        A_service=1
                                        service = rvalue
						
						

          elif(tag[i].contents[j].name == "ul"):
            if (tag[i].contents[j]['class']=="stayNfo"): #stayNfo
              for k in xrange(0, len(tag[i].contents[j].contents)):
                if not isinstance(tag[i].contents[j].contents[k], unicode):
		  if(tag[i].contents[j].contents[k].name =="li"):
                    for l in xrange(0, len(tag[i].contents[j].contents[k].contents)):
                      if isinstance(tag[i].contents[j].contents[k].contents[l], unicode):
                        info_data=str( tag[i].contents[j].contents[k].contents[l])
			info_data = info_data.lstrip(' ')
			info_data = info_data.replace('\n', ' ')
                        info_data = info_data.replace('\'', ' ')
	 	 	info_data = info_data.replace('(' , ' ')
			info_data = info_data.replace(')' , ' ')

                      elif(tag[i].contents[j].contents[k].contents[l].name =="b"):
                        for m in xrange(0, len(tag[i].contents[j].contents[k].contents[l].contents)):
                          if isinstance(tag[i].contents[j].contents[k].contents[l].contents[m], unicode):
                            info_type=str( tag[i].contents[j].contents[k].contents[l].contents[m] )
                            info_type=info_type.lstrip('')
                            info_type=info_type.replace('\n', '')
		    if(info_type=='Date of stay'):
		      dos = info_data
		      A_dos = 1
		    if(info_type=='Visit was for'):
	 	      vwf = info_data
	              A_vwf = 1
		    if(info_type=='Traveled with'):
	              tw = info_data
		      A_tw = 1

      if(A_review == 1):
	string = 'insert into '+filename+ ' values (' + '\''+str(review_no)+'\', ' + '\''+review+'\', '
	if (A_triptype==1):
          string += '\''+triptype+'\', '
        else:
	  string += 'NULL'+', '
	if (A_rating==1):
          string += '\''+rating+'\', '
        else:
          string += 'NULL'+', '
        if (A_value == 1):
          string += '\''+value+'\', ' 
        else:
 	  string += 'NULL'+', ' 
        if (A_rooms == 1):
	  string += '\''+rooms+'\', '
	else:
	  string += 'NULL'+', '
        if (A_location == 1):
	  string += '\''+location+'\', '
	else:
	  string += 'NULL'+', '
        if (A_cleanliness == 1):
	  string += '\''+cleanliness+'\', '
	else:
	  string += 'NULL'+', '
        if (A_service == 1):
	  string += '\''+service+'\', '
	else:
	  string += 'NULL'+', '
        if (A_dos==1):
	  string += '\''+dos+'\', '
	else:
	  string += 'NULL'+', '
        if (A_vwf == 1):
	  string += '\''+vwf+'\', '
	else:
	  string += 'NULL'+', '
        if (A_tw == 1):
	  string += '\''+tw+'\')'
	else:
	  string += 'NULL)'
	try:
	  con.execute(string)
	except Exception, er:
	  print er


#--------------------link to next page-----------------------------------------
    link = soup.find('a', attrs={'class' : re.compile("^util2$")})
    if(soup.find('a', attrs={'class' : re.compile("^util2$")})==None):
      flag=0
    else:
      counter=0
      while True:
        try:
          print "Opening..." + 'http://www.tripadvisor.com' + link['href']
          file = urllib2.urlopen('http://www.tripadvisor.com' + link['href'])
          break
        except urllib2.HTTPError, e:
   	  if (e.code==403):
	    print e.code
	    flag=0
	    break
	  elif(e.code==404):
            print e.code
            flag=0
	    break
	  elif(e.code==408):
	    print e.code
            counter = counter + 1
            if(counter > 5):
              flag=1
              break
	  elif(e.code==500):
	    print e.code
            counter = counter + 1
            if(counter > 5):
              flag=1
              break
	  elif(e.code==503):
	    print e.code
            counter = counter + 1
            if(counter > 5):
              flag=1
              break
	  elif(e.code==504):
	    print e.code
            counter = counter + 1
            if(counter > 5):
              flag=1
              break
          elif(e.code==104):
            print e.code
            counter = counter + 1
            if(counter > 5):
              flag=1
              break
          else:
            print e.code
            counter = counter +1
            if(counter > 5):
              flag=1
              break
        except urllib2.URLError, e:
          print e.reason
          counter = counter + 1
          if(counter > 5):
            flag=1
            break
     

f1.close()

print "Finish\n"
