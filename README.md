Ubik Sentiment
===============

The project creates a simple machine learning model to classify positive or negative 
emotion of a given sentence. 

The training data is in finnish and generated from Korppi with a simple heuristic. 
[Korppi](https://korp.csc.fi/) corpus API is searched for sentences containing happy
smile  ':)' and sad smileys ':(' which are assumed to note for positive and negative 
sentiments respectively.

To evaluate the model's feasibility for real world use a simple annotation tool is
can be used to annotate data for evaluation. 

A cli tool is provided the test the sentiment of a sentence:

```sh
$ python test_sentence.py

Anna lause: Auto ei ollutkaan niin hyväkuntoinen kun myyjä antoi ymmärtää
['neg']
Anna lause: Pahemmastakin suosta on noustu
['pos']

```

# Installation

Create some training and test data if you don't have it already.

To get some finnish language raw smiley data from Korppi:

```sh

$ python fetch_rawdata.py > korp_all_sentences.txt

```

Then process it to create training and development sets and data to annotate into evaluation set:

```sh

$ generate_sets.sh

```

Then process it to create training and development sets and data to annotate into evaluation set:
If you want to create human annotated evaluation set, use annotate.py:

```sh

$ python annotate.py
To annotate lines, press p for positive, n for negative, any other letter to discard. Q to quit.

siis koitas perheen kans vaikkapa ihan perinteistä munien maalaamista
pos
leivo jotain tai saahan sitä kaupoista valmistakin
quit

Annotated 1 positives and 0 negative sentences. Discarded 0 rows.
In total 1 sentences have been processed.

```

Next create the model.

```sh

$ python train_classifier.py

Warning: enforcing limit of 10000 samples to dataset ./data/korp_train_pos.txt
Warning: enforcing limit of 10000 samples to dataset ./data/korp_devel_pos.txt
Found 14768 training sentences, 12330 development testing sentences.
Creating a vectorizer...
Vectorizing training set...
Vectorizing development set...
Evaluating the best hyperparameter C...

Best C value is 0.03125 with the accuracy of 0.8261151662611517.
Saving vectorizer and classifier...
Done.

```

Finally try the model with a sentence.

```sh

$ python test_sentence.py 

```

# Work definitions for positive and negative emotions

For purposes of manual annotation of evaluation data the following definition was used:

Negative sentiment contains
 - negative emotions such as anger or sadness
 - uncertainty, confusion
 - anti-social behaviour such as judging, calling names or insulting others
 - contains cursing or vulgarity

Positive sentiment contains
 - positive emotions such as excitement or happiness
 - encouraging, hopeful or helpful behaviour
 
# Author

- [tjkemp](https://github.com/tjkemp)

Distributed under the MIT license. See ``license.txt`` for more information.
