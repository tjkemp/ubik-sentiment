#!/bin/sh

# This shell scripts cleans a little bit the raw smiley data got with: 
# python ./fetch_rawdata.py > korp_all_sentences.txt
# and then creates training and development sets and eval file for annotation

tempfile_clean=$(mktemp)
tempfile_train=$(mktemp)
tempfile_half=$(mktemp)
tempfile_devel=$(mktemp)
tempfile_eval=$(mktemp)

# 1. remove lines with only either :) or :( smiley and then shuffle data
cat korp_all_sentences.txt | grep -Pv "^:\)$|^:\($" > ${tempfile_clean}

# 2. divide the data to training set (1/2) and development set (1/4)
# and a set from which to annotate an evaluation set (1/4)

len_total=$(wc -l $tempfile_clean| awk '{print $1}')
len_half=$(expr $len_total / 2)
len_quarter=$(expr $len_half / 2)

# create training sets
cat ${tempfile_clean} | head -${len_half} > ${tempfile_train}

cat ${tempfile_train} | grep ":)"| perl -pe 's/\:\)//g' >  korp_train_pos.txt
cat ${tempfile_train} | grep ":("| perl -pe 's/\:\(//g' >  korp_train_neg.txt

# split rest into devel and eval
cat ${tempfile_clean} | tail -${len_half} > ${tempfile_half}
cat ${tempfile_half} | head -${len_quarter} > ${tempfile_devel}
cat ${tempfile_half} | tail -${len_quarter} > ${tempfile_eval}

# create development sets

cat ${tempfile_devel} | grep ":)"| perl -pe 's/\:\)//g' >  korp_devel_pos.txt
cat ${tempfile_devel} | grep ":("| perl -pe 's/\:\(//g' >  korp_devel_neg.txt

# create raw data to be annotated as evaluation sets

cat ${tempfile_eval} | perl -pe 's/\:\(//g' | perl -pe 's/\:\)//g' > korp_eval_raw.txt

# 3. clean up

# delete temporary files
rm ${tempfile_clean}
rm ${tempfile_train}
rm ${tempfile_half}
rm ${tempfile_devel}
rm ${tempfile_eval}
