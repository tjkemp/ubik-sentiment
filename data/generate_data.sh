#!/bin/sh

# Uncomment to fetch original data
#python ./korp_api.py > korp_lauseet.txt

cat korp_lauseet.txt | grep -Pv "^:\)$|^:\($" > deleteme_clean.txt
cat deleteme_clean.txt | shuf > deleteme_shuffle.txt

# divide it to train and test sets
len_total=$(wc -l deleteme_shuffle.txt| awk '{print $1}')
len_testset=$(expr $len_total / 5)
len_trainset=$(expr $len_total - $len_testset)

cat deleteme_shuffle.txt | head -$len_trainset > deleteme_train.txt
cat deleteme_shuffle.txt | tail -$len_testset > deleteme_test.txt

# divide sets into negative and positive sentiment sets
cat deleteme_train.txt |grep ":)"|perl -pe 's/\:\)//g' >  korp_train_pos.txt
cat deleteme_train.txt |grep ":("|perl -pe 's/\:\(//g' >  korp_train_neg.txt
cat deleteme_test.txt |grep ":)"|perl -pe 's/\:\)//g' >  korp_test_pos.txt
cat deleteme_test.txt |grep ":("|perl -pe 's/\:\(//g' >  korp_test_neg.txt

# clean up
rm deleteme_*.txt
