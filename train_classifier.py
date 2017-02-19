#!/bin/python

import codecs
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
import pprint
import pickle

def load_data(classes=['pos', 'neg'], dataset='smiley'):
    sentences = []
    labels = []
    for c in classes:
        lan_sentences = codecs.open('./data/%s_%s.txt' % (dataset, c), 'r', 'utf-8').readlines()
        sentences += [s.strip() for s in lan_sentences]
        labels += [c] * len(lan_sentences)

    return sentences, labels

# load data sets
train_sentences, train_labels = load_data(dataset='korp_train')
test_sentences, test_labels = load_data(dataset='korp_test')

# convert sentences to feature vectors
print ("Creating a vectorizer...")
vectorizer = TfidfVectorizer(analyzer='word', norm='l2')
vectorizer.fit(train_sentences)

print ("Vectorizing training set...")
train_vectors = vectorizer.transform(train_sentences).toarray()
print ("Vectorizing test set...")
test_vectors = vectorizer.transform(test_sentences).toarray()

# test for the best classifier
score_best = 0.0
c_best = -1
classifier_best = None
print ("Evaluating the best hyperparameter C...")
for i in range (-10, 10):
  c = 2**i
  classifier = LinearSVC(C=c)
  classifier.fit(train_vectors, train_labels)
  score = accuracy_score(test_labels, classifier.predict(test_vectors))
  if score > score_best:
    c_best = c
    score_best = score
    classifier_best = classifier
  print ("With C = %s test set accuracy: %s." % (c, score))

print ("Best C value is %s with the accuracy of %s." % (c_best,score_best))

# save the best classifier
print ("Saving vectorizer and classifier...")
with open('vectorizer.pickle', 'wb') as f:
    pickle.dump(vectorizer, f, pickle.HIGHEST_PROTOCOL)
with open('classifier.pickle', 'wb') as f:
    pickle.dump(classifier_best, f, pickle.HIGHEST_PROTOCOL)
print ("Done.")
