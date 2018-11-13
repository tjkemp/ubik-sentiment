Ubik Sentiment repository
=========================

This project creates a simple model to classify positivity or negativity of a given sentence. 

The training data could be got from anywhere but it should be a list of sentences annotated as
either positive or negative.

In this example the training data generated from Korppi data with a simpler heuristic. The corpus
API is searched for sentences containing happy smile ':)' and sad smileys ':(' which we are assumed
to be positive and negative sentences respectively and thus note for positive or negative sentiments.

A cli tool is provided the test a sentence:

```sh
$ python test_sentence.py

Anna lause: Auto ei ollutkaan niin hyväkuntoinen kun myyjä antoi ymmärtää
['neg']
Anna lause: Pahemmastakin suosta on noustu
['pos']

```

Installation
--------------

Create some training and test data if you don't have it already.

To get some finnish language raw smiley data from Korppi:

```sh
$ cd data

$ python fetch_rawdata.py

```

Then process it to training and test data:

```sh

$ generate_trainingsets.sh

```

Next creating a model.

Note that example output below is created with just hundreds of rows of training data hence the bad results.

```sh

$ python train_classifier.py

Creating a vectorizer...
Vectorizing training set...
Vectorizing test set...
Evaluating the best hyperparameter C...
With C = 0.0009765625 test set accuracy: 0.6633333333333333.
With C = 0.001953125 test set accuracy: 0.6616666666666666.
With C = 0.00390625 test set accuracy: 0.6633333333333333.
With C = 0.0078125 test set accuracy: 0.665.
With C = 0.015625 test set accuracy: 0.67.
With C = 0.03125 test set accuracy: 0.67.
With C = 0.0625 test set accuracy: 0.67.
With C = 0.125 test set accuracy: 0.67.
With C = 0.25 test set accuracy: 0.6683333333333333.
With C = 0.5 test set accuracy: 0.6716666666666666.
With C = 1 test set accuracy: 0.67.
With C = 2 test set accuracy: 0.6566666666666666.
With C = 4 test set accuracy: 0.655.
With C = 8 test set accuracy: 0.6533333333333333.
With C = 16 test set accuracy: 0.6583333333333333.
With C = 32 test set accuracy: 0.6533333333333333.
With C = 64 test set accuracy: 0.6533333333333333.
With C = 128 test set accuracy: 0.6516666666666666.
With C = 256 test set accuracy: 0.6566666666666666.
With C = 512 test set accuracy: 0.6566666666666666.

Best C value is 0.5 with the accuracy of 0.6716666666666666.
Saving vectorizer and classifier...
Done.

```

Finally try the model a sentence:

```sh

$ python test_sentence.py 

```


Author
-------

- [tjkemp](https://github.com/tjkemp)

Distributed under the MIT license. See ``license.txt`` for more information.
