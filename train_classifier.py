from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
import codecs

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

def main():
    # load data sets
    train_sentences, train_labels = load_data(dataset='korp_train')
    test_sentences, test_labels = load_data(dataset='korp_devel')

    print("Found {} training sentences, {} test sentences.".format(len(train_sentences), len(test_sentences)))

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
        score_train = accuracy_score(train_labels, classifier.predict(train_vectors))
        score_test = accuracy_score(test_labels, classifier.predict(test_vectors))
        if score_test > score_best:
            c_best = c
            score_best = score_test
            classifier_best = classifier
        print ("With C = %s with test set accuracy: %s (and training set accuracy: %s)." % (c, score_test, score_train))

    print ("Best C value is %s with the accuracy of %s." % (c_best, score_best))

    # save the best classifier
    print ("Saving vectorizer and classifier...")
    joblib.dump(vectorizer, 'model/vectorizer.joblib')
    joblib.dump(classifier_best, 'model/classifier.joblib')
    print ("Done.")

if __name__ == "__main__":
    main()