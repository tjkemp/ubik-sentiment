import sys
import codecs
import importlib
import warnings
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib

def load_data(classes=['pos', 'neg'], dataset='unknown', limit=1000):
    sentences = []
    labels = []
    for class_ in classes:
        filename = './data/%s_%s.txt' % (dataset, class_)
        lan_sentences = codecs.open(filename, 'r', 'utf-8').readlines()
        if len(lan_sentences) > limit:
            print(f"Warning: enforcing limit of {limit} samples to dataset {filename}")
        sentences += [s.strip() for s in lan_sentences[:limit]]
        label_count = len(lan_sentences) if len(lan_sentences) < limit else limit
        labels += [class_] * label_count

    return sentences, labels

def main(limit=1000):

    # supress deprecation warnings by joblib
    warnings.simplefilter('ignore')
    
    # load data sets
    train_sentences, train_labels = load_data(dataset='korp_train', limit=limit)
    devel_sentences, devel_labels = load_data(dataset='korp_devel', limit=limit)

    print("Found {} training sentences, {} test sentences.".format(len(train_sentences), len(devel_sentences)))

    # convert sentences to feature vectors
    print ("Creating a vectorizer...")
    vectorizer = TfidfVectorizer(analyzer='word', norm='l2')
    vectorizer.fit(train_sentences)

    print ("Vectorizing training set...")
    train_vectors = vectorizer.transform(train_sentences).toarray()
    print ("Vectorizing test set...")
    devel_vectors = vectorizer.transform(devel_sentences).toarray()

    classifier = MultinomialNB()
    classifier.fit(train_vectors, train_labels)
    score_train = accuracy_score(train_labels, classifier.predict(train_vectors))
    score_devel = accuracy_score(devel_labels, classifier.predict(devel_vectors))

    print (f"Accuracy: {score_devel:.3f} (devel set), {score_train:.3f} (training set).")

    # save the best classifier
    print ("Saving vectorizer and classifier...")
    joblib.dump(vectorizer, 'model/vectorizer.joblib')
    joblib.dump(classifier, 'model/classifier.joblib')
    print ("Done.")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(limit=int(sys.argv[1]))
    else:
        print("Usage: python train_classifier.py <class_max_length>")
