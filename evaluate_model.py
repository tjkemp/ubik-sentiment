from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.externals import joblib
import codecs

def load_data(classes=['pos', 'neg'], dataset='unknown'):
    sentences = []
    labels = []
    for class_ in classes:
        filename = './data/%s_%s.txt' % (dataset, class_)
        lan_sentences = codecs.open(filename, 'r', 'utf-8').readlines()
        sentences += [s.strip() for s in lan_sentences]
        labels += [class_] * len(lan_sentences)

    return sentences, labels

def print_cm(matrix, labels):
    print()
    print("Confusion matrix:")
    print(f"\t{labels[0]}\t{labels[1]}")
    print(f"{labels[0]}\t{matrix[0][0]}\t{matrix[0][1]}") 
    print(f"{labels[1]}\t{matrix[1][0]}\t{matrix[1][1]}") 

def main():

    # load previously generated vectorizer and classifier
    vectorizer = joblib.load('model/vectorizer.joblib')
    classifier = joblib.load('model/classifier.joblib')

    # load sentences to predict
    eval_sentences, eval_labels = load_data(dataset='korp_devel')
    predict_vectors = vectorizer.transform(eval_sentences).toarray()
    predictions = classifier.predict(predict_vectors)
    score_eval = accuracy_score(eval_labels, predictions)

    print(f"On the dataset the model has the accuracy of {score_eval:.3f}.")

    labels = ["pos", "neg"]
    cm = confusion_matrix(eval_labels, predictions, labels=labels)
    print_cm(cm, labels)

if __name__ == "__main__":
    main()