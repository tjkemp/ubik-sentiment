from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
import pickle

def load_sentences(dataset='Turku'):
    sentences = []
    lan_sentences = codecs.open('./cities/%s.txt' % (dataset), 'r', 'utf-8').readlines()
    sentences += [s.strip() for s in lan_sentences]

    return sentences

# load previously generated vectorizer and classifier
with open('test/vectorizer.pickle', 'rb') as f:
    vectorizer = pickle.load(f)
with open('test/classifier.pickle', 'rb') as f:
    classifier = pickle.load(f)

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
