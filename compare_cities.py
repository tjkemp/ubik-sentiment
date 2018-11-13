from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
import codecs

def load_sentences(dataset='Turku'):
    sentences = []
    lan_sentences = codecs.open('./cities/%s.txt' % (dataset), 'r', 'utf-8').readlines()
    sentences += [s.strip() for s in lan_sentences]

    return sentences

def main():
    #
    # NOTE: this file is under development
    #

    # load previously generated vectorizer and classifier
    vectorizer = joblib.load('model/vectorizer.joblib')
    classifier = joblib.load('model/classifier.joblib')

    # load sentences to predict
    datasets = ['Rauma', 'Kotka', 'Lappeenranta', 'Rovaniemi']

    for dataset in datasets:
        predict_sentences = load_sentences(dataset=dataset)

        predict_vectors = vectorizer.transform(predict_sentences)

        predictions = classifier.predict(predict_vectors)
        pred_pos = (predictions == 'pos').sum()
        pred_neg = (predictions == 'neg').sum()

        print("Dataset {} has {} positive and {} negative sentences with positivity % of {:.2f}.").format(
            dataset, pred_pos, pred_neg, (float(pred_pos) / (pred_pos+pred_neg))*100)

if __name__ == "__main__":
    main()