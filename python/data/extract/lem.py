#Program name : lem.py
#Author       : LAM Wai Man
#Student ID   : 07010702
#Description  : To demonstrate the difference of lemmatized and non lemmatized words.
#Input        : btagger.dat
#Output       : Screen standard output
#Usage        : $python lem.py



import nltk
import nltk.corpus.reader.wordnet
import pickle


wcr = nltk.corpus.reader.wordnet.WordNetCorpusReader('/usr/share/nltk_data/corpora/wordnet')

fin = open("btagger.dat", "rb")
tagger = pickle.load(fin)
fin.close()


#raw = """this is just as a note that a new hotel had openned up in the same building as the accelerator international hotel . the new hotel is called the sunny day hotel  the second hotel of this name in hk . the other one is in reclaimation st in mongkok . the telephone number of the sunny day hotel is different  i am not sure at this stage whether the accelerator have been renovated and had it name changed or whether the sunny day hotel is a new hotel coincidentially in the same building ."""

raw = """this hotel is just perfect,nothing was less than perfect :
the conrad is really a fabulous hotel. service is top-notch , all employees are doing their best to help and they really made us enjoy our short stay. upon check-in , we were upgraded to a small suite , which was a nice attention... ."""

tokens = nltk.word_tokenize(raw)
print "Original:"
print tokens

taglist = tagger.tag(tokens)
tokens2 = []
for k in range(0, len(taglist)-1):
      if 'ADJ' in taglist[k][1]:
       t=wcr.morphy(taglist[k][0],'a')
       if not t:
        tokens2.append(taglist[k][0])
       else:
        tokens2.append(t)
      elif 'VB' in taglist[k][1]:
       t=wcr.morphy(taglist[k][0],'v')
       if not t:
        tokens2.append(taglist[k][0])
       else:
        tokens2.append(t)
      elif 'NN' in taglist[k][1]:
       t=wcr.morphy(taglist[k][0],'n')
       if not t:
        tokens2.append(taglist[k][0])
       else:
        tokens2.append(t)
      else:
       tokens2.append(taglist[k][0])
 

print "\nAfter lemmatization:"
print tokens2
#print [wcr.morphy(t) for t in tokens]2
