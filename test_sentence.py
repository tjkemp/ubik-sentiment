from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib

def main():

    # load previously generated vectorizer and classifier
    vectorizer = joblib.load('model/vectorizer.joblib')
    classifier = joblib.load('model/classifier.joblib')

    while (True):
        sentence = input("Anna lause: ")

        predict_vector = vectorizer.transform([sentence])

        prediction = classifier.predict(predict_vector)

        print(prediction)

if __name__ == "__main__":
    main()