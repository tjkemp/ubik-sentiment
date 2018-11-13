from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
import pickle

# load previously generated vectorizer and classifier
with open('test/vectorizer.pickle', 'rb') as f:
    vectorizer = pickle.load(f)
with open('test/classifier.pickle', 'rb') as f:
    classifier = pickle.load(f)

while (True):
    sentence = raw_input("Anna lause: ")

    predict_vector = vectorizer.transform([sentence])

    prediction = classifier.predict(predict_vector)

    print (prediction)
