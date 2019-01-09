import os
import codecs
import operator
import json
import itertools
import numpy as np

def load_data(dataset='unknown', 
            location='./data/', 
            maxlen=None,
            seed=1234,
            limit_cls=1000):
    """ Loads a dataset. 
    
    Expects dataset to exist in 'location' directory as file 'dataset.npy'.

    Arguments:
        maxlen : integer, sequences longer than this will be skipped
        seed : integer, seed for random shuffling
        limit_cls : integer, limit on how many sequences is retrieved per class
    
    Returns:
        tuple of numpy arrays: (x, y)

    """

    filename = dataset + ".npy"
    path = os.path.join(location, filename)
    data = np.load(path)
    sentences, labels = data[0], data[1]
    return sentences, labels

def prepare_data(classes=['neg', 'pos'], 
            dataset='unknown', 
            location='./data/', 
            seed=1234):
    """ Loads raw strings and writes it as a a dataset. 
    
    Expects a dataset in '{location}' as files '{dataset}_{class}.txt'.

    Arguments:
        seed : integer, seed for random shuffling

    Side-effects:
        Writes files '{dataset}.npz' with the training data as numbers
        and '{dataset}_index.json' as index to the meaning of numbers.

    Note that sentences should already be tokenized.

    """
    sentences = []
    labels = []

    word_counts = {}
    word_index = {}

    # 1. first get all sentences
    for idx, class_ in enumerate(classes):

        filename = "{}_{}.txt".format(dataset, class_)
        path = os.path.join(location, filename)
        sentences_cls = codecs.open(path, 'r', 'utf-8').readlines()

        # NOTE the strings are turned to lower case, should they?
        # NOTE should there be a maxlen for a sentence?
        #sentences += [list(map(str.lower, s.strip())) for s in sentences_cls]
        for sentence in sentences_cls:
            sentence = sentence.strip().lower()
            items = sentence.split()
            sentences += [items]
        labels += [idx] * len(sentences_cls)

    # 2. count all the words
    for words in sentences:
        for word in words:
            try:
                word_counts[word] += 1
            except KeyError:
                word_counts[word] = 1

    # 3. then give an index number to each words depending how common they are
    # build in somme indices as convention: 
    # 0 -> padding, 1 -> start, 2 -> OOV (words that were cut out)

    # NOTE consider removing these indices

    for idx, (word, count) in enumerate(
            sorted(word_counts.items(), key=operator.itemgetter(1), reverse=True),
            start=3):
        word_index[word] = idx

    # 4. convert sentences with labels to numbers    
    encoded_sentences = []
    for idx, words in enumerate(sentences):
        encoded = [word_index[word] for word in words]
        #encoded_data.append([1] + encoded_sentence)
        encoded_sentences.append(encoded)

    # 5. save everything

    # training data
    encoded_sentences = np.array(encoded_sentences)
    labels = np.array(labels, dtype=np.int8)
    data = np.array([encoded_sentences, labels])

    path = os.path.join(location, dataset)
    np.save(path, data)

    # word indices
    filename = "{}_index.txt".format(dataset)
    path = os.path.join(location, filename)
    with codecs.open(path, 'w', encoding="utf-8") as output:
        json.dump(word_index, output, ensure_ascii=False)

    # word counts
    filename = "{}_words.txt".format(dataset)
    path = os.path.join(location, filename)
    with open(path, 'w', encoding="utf-8", errors='replace') as output:
        for word, count in sorted(word_counts.items(), key=operator.itemgetter(1), reverse=True):
            output.write(f"{count} {word}\n")

def get_index(dataset='unknown', location='./data/'):
    """Retrieves the dictionary mapping word to word indices.

    Arguments
        path: where to cache the data (relative to `~/.keras/dataset`).
    Returns
        The word index dictionary.
    """
    filename = "{}_index.txt".format(dataset)
    path = os.path.join(location, filename)
    with codecs.open(path, 'r', encoding="utf-8") as output:
        word_index = json.load(output)

    return word_index

# Helper functions

def max_value(np_array):
    """ Returns the length of the longest sentence. """
    return max([max(item) for item in np_array])

def get_word_decoder(train_data, word_index):
    """ Returns a function that can decode a sentence. """
    reverse_word_index = dict(
        [(value, key) for (key, value) in word_index.items()])
    def reverse(idx):
        return " ".join([reverse_word_index.get(i, '?') for i in train_data[idx]])
    return reverse

def vectorize_sequence(sequences, dimension):
    """ Turns sequences into vectors of 0s and 1s. """
    results = np.zeros((len(sequences), dimension))
    for i, seq in enumerate(sequences):
        results[i, seq] = 1.
    return results

if __name__ == "__main__":
    prepare_data(dataset='korp_devel')
