#!/bin/sh

# Perspective API initialization script.

HOME=$(pwd)

echo "Perspective API: Testing..."
python perspective.py

cd $HOME
