#!/bin/sh

HOME=$(pwd)

echo "Installing Python dependencies..."
python -m pip install -r requirements.txt

./init_twitteraae.sh
./init_wtc_pa.sh
./init_perspective.sh

cd $HOME
