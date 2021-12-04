#!/bin/sh
# Cleans up non-essential local files.

echo "Cleanup up TwitterAAE"

# Files
rm -vf attack_annotated_comments.tsv
rm -vf attack_annotations.tsv
rm -vf master.zip

# Folders
rm -vrf twitteraae/
