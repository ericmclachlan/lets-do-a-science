#!/bin/sh
# Cleans up non-essential local files.

echo "Cleanup up TwitterAAE"

# Files
rm -vf master.zip
rm -vf *.tsv

# Folders
rm -vrf twitteraae/
