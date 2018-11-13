#!/bin/sh

# Uncomment to fetch original data
#python ./korp_api.py > korp_lauseet.txt

# 1. extract data with either :) or :( smiley
cat korp_lauseet.txt | grep -Pv "^:\)$|^:\($" > temp_clean.txt

# 2. shuffle the data
cat temp_clean.txt | shuf > temp_shuffle.txt

# 3. divide the data to training set (2/3) and test set (1/3)
len_total=$(wc -l temp_shuffle.txt| awk '{print $1}')

len_testset=$(expr $len_total / 3)
len_trainset=$(expr $len_total - $len_testset)

cat temp_shuffle.txt | head -$len_trainset > temp_train.txt
cat temp_shuffle.txt | tail -$len_testset > temp_test.txt

# 4. remove smileys and divide sets into negative and positive sentiment sets
cat temp_train.txt |grep ":)"|perl -pe 's/\:\)//g' >  korp_train_pos.txt
cat temp_train.txt |grep ":("|perl -pe 's/\:\(//g' >  korp_train_neg.txt
cat temp_test.txt |grep ":)"|perl -pe 's/\:\)//g' >  korp_test_pos.txt
cat temp_test.txt |grep ":("|perl -pe 's/\:\(//g' >  korp_test_neg.txt

# delete temporary files
rm temp_*.txt
