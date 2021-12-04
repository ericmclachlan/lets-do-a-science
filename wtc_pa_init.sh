#!/bin/sh

# Wikipedia Talk Corpus: Personal Attack initialization script.

HOME=$(pwd)

echo "Wikipedia Talk Corpus: Downloading attack_annotated_comments.tsv..."
wget -O attack_annotated_comments.tsv https://figshare.com/ndownloader/files/7554634

echo "Wikipedia Talk Corpus: Downloading attack_annotations.tsv..."
wget -O attack_annotations.tsv https://figshare.com/ndownloader/files/7554637

# echo "Wikipedia Talk Corpus: Testing..."
python wtc_pa_test.py

cd $HOME
