#Program name : tagger.py
#Author       : LAM Wai Man
#Student ID   : 07010702
#Description  : To train a brill tagger to later usage.
#Input        : from nltk corpora
#Output       : btagger.dat
#Usage        : $python tagger.py



import nltk.tag
from nltk.tag import brill
import nltk.corpus, nltk.tag, itertools
from nltk.corpus import brown, conll2000, treebank
import pickle
import time

timevar3 = time.time()

def backoff_tagger(tagged_sents, tagger_classes, backoff=None):
	if not backoff:
		backoff = tagger_classes[0](tagged_sents)
		del tagger_classes[0]

	for cls in tagger_classes:
		tagger = cls(tagged_sents, backoff=backoff)
		backoff = tagger

	return backoff

word_patterns = [
	(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
	(r'.*ould$', 'MD'),
	(r'.*ing$', 'VBG'),
	(r'.*ed$', 'VBD'),
	(r'.*ness$', 'NN'),
	(r'.*ment$', 'NN'),
	(r'.*ful$', 'JJ'),
	(r'.*ious$', 'JJ'),
	(r'.*ble$', 'JJ'),
	(r'.*ic$', 'JJ'),
	(r'.*ive$', 'JJ'),
	(r'.*ic$', 'JJ'),
	(r'.*est$', 'JJ'),
	(r'^a$', 'PREP'),
]



#brown_reviews = brown.tagged_sents(categories=['reviews'],simplify_tags=True)
#brown_reviews_cutoff = len(brown_reviews) * 2 / 3
#brown_lore = brown.tagged_sents(categories=['lore'],simplify_tags=True)
#brown_lore_cutoff = len(brown_lore) * 2 / 3
#brown_romance = brown.tagged_sents(categories=['romance'],simplify_tags=True)
#brown_romance_cutoff = len(brown_romance) * 2 / 3
#brown_fiction = brown.tagged_sents(categories=['fiction'],simplify_tags=True)
#brown_fiction_cutoff = len(brown_fiction) * 2 / 3
#brown_belles_lettres = brown.tagged_sents(categories=['belles_lettres'],simplify_tags=True)
#brown_belles_lettres_cutoff = len(brown_belles_lettres) * 2 / 3



#brown_train = list(itertools.chain(brown_reviews[:brown_reviews_cutoff],
#	brown_lore[:brown_lore_cutoff], brown_romance[:brown_romance_cutoff],brown_fiction[:brown_fiction_cutoff],
#        brown_belles_lettres[brown_belles_lettres_cutoff:]))
#brown_test = list(itertools.chain(brown_reviews[brown_reviews_cutoff:],
#	brown_lore[brown_lore_cutoff:], brown_romance[brown_romance_cutoff:],brown_fiction[:brown_fiction_cutoff],
#        brown_belles_lettres[brown_belles_lettres_cutoff:]))

conll_train = conll2000.tagged_sents('train.txt')
conll_test = conll2000.tagged_sents('test.txt')

treebank_cutoff = len(treebank.tagged_sents()) * 2 / 3
treebank_train = treebank.tagged_sents()[:treebank_cutoff]
treebank_test = treebank.tagged_sents()[treebank_cutoff:]

train_sents = conll_train +  treebank_train
test_sents  = conll_test  + treebank_test
#train_sents = brown_train
#test_sents = treebank_test

#print test_sents
raubt_tagger = backoff_tagger(train_sents, [nltk.tag.AffixTagger,
    nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger],
    backoff=nltk.tag.DefaultTagger('NN'))

templates = [
    brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (1,1)),
    brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (2,2)),
    brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (1,2)),
    brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (1,3)),
    brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (1,1)),
    brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (2,2)),
    brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (1,2)),
    brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (1,3)),
    brill.ProximateTokensTemplate(brill.ProximateTagsRule, (-1, -1), (1,1)),
    brill.ProximateTokensTemplate(brill.ProximateWordsRule, (-1, -1), (1,1))
]

print "training tagger..."
timevar1 = time.time()
trainer = brill.FastBrillTaggerTrainer(raubt_tagger, templates)
braubt_tagger = trainer.train(train_sents, max_rules=100, min_score=3)

print braubt_tagger.evaluate(test_sents)
timevar2 = time.time()
print(timevar2-timevar1)

tagger2 = braubt_tagger
fout = open("./tagger6.dat", "wb")
# default protocol is zero
# -1 gives highest prototcol and smallest data file size
pickle.dump(tagger2, fout, protocol=-1)
fout.close()


