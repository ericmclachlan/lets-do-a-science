#!/bin/sh

HOME=$(pwd)

echo "TwitterAAE: Downloading..."
wget https://github.com/slanglab/twitteraae/archive/refs/heads/master.zip

echo "TwitterAAE: Preparing..."
unzip master.zip
mv twitteraae-master twitteraae

echo "TwitterAAE: Upgrading to Python 3..."
cp twitteraae.patch.diff twitteraae
cp twitteraae.py twitteraae/code/
cd twitteraae
patch -p1 < twitteraae.patch.diff

echo "TwitterAAE: Testing..."
cd code
python twitteraae.py

cd $HOME
