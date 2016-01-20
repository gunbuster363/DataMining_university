from nltk.corpus import movie_reviews
import random
import nltk
import pickle
from operator import itemgetter


def sort_dict2list(d):
	items = [(v, k) for k, v in d.items()]
	items.sort()
	items.reverse()
	items = [(k, v) for v, k in items]
	list = [w[0] for w in items]
	return list

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


fin = open("class.dat", "rb")
documents = pickle.load(fin)
fin.close()

fin = open("list.dat", "rb")
dict = pickle.load(fin)
fin.close()



print "document length:"
print len(documents)
print "dict length"
print len(dict)

wordlist = sort_dict2list(dict)

random.shuffle(documents)

word_features = wordlist[:2000]


featuresets = [(document_features(d), c) for (d,c) in documents]
train_set, test_set = featuresets[:1000], featuresets[1001:]

print "training..."
classifier = nltk.NaiveBayesClassifier.train(train_set)

print "testing..."
print nltk.classify.accuracy(classifier, test_set)

print classifier.classify(document_features("I am stay here with my girlfriend."))
print classifier.show_most_informative_features(20) 

k=0
for w in documents:
 if(k<50):
   print classifier.classify(document_features(w[0]))
 k=k+1

