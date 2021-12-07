#!/bin/sh

# A script for automating the execution of the experiement.

HOME=$(pwd)

python wtc_pa.py add_annotations wtc_pa_with_annotations.tsv

cd twitteraae/code
python twitteraae.py add_constituents

cd $HOME

python perspective.py add_perspective
