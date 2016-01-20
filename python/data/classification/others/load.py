from nltk.corpus import movie_reviews
import random
import nltk
import pickle
from operator import itemgetter


fin = open("../triptype/triptype.dat", "rb")
documents = pickle.load(fin)
fin.close()


newlist =[]
for i in range(0, len(documents)-1):
 if(len(documents[i][0])!=0):
  newlist.append(documents[i])
 else:
  print "Stripped"
  #print documents[i] 

print "done"

for i in range(0, len(newlist)-1):
 if(len(newlist[i][0])==0):
  print "still something here"


fout = open("../triptype/triptype.dat", "wb")
# default protocol is zero
# -1 gives highest prototcol and smallest data file size
pickle.dump(newlist, fout, protocol=-1)
fout.close()

