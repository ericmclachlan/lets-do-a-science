"""
A module for testing the readability of the Wikipedia Talk Corpus: Personal Attack corpus.

Heavily inspired by a Jupyter notebook template provided here:
    https://github.com/ewulczyn/wiki-detox/blob/master/src/figshare/Wikipedia%20Talk%20Data%20-%20Getting%20Started.ipynb

"""


import pandas as pd

# Constants

ATTACK_ANNOTATIONS_FILE = "attack_annotations.tsv"
ATTACK_ANNOTATED_COMMENTS_FILE = "attack_annotated_comments.tsv"
SAMPLES_TO_SHOW=10


# Loads the comments and annotations files.
print("Wikipedia Talk Labels: Personal Attacks: Loading...")
comments = pd.read_csv('attack_annotated_comments.tsv', sep = '\t', index_col = 0)
annotations = pd.read_csv('attack_annotations.tsv',  sep = '\t')

# print(len(comments['rev_id'].unique()))
print(f"No of comments annotated: {len(annotations['rev_id'].unique())}")

# Annotations by majority voting.
labels_attack = annotations.groupby('rev_id')['attack'].mean() > 0.5
labels_recipient_attack = annotations.groupby('rev_id')['recipient_attack'].mean() > 0.5
labels_third_party_attack = annotations.groupby('rev_id')['third_party_attack'].mean() > 0.5

# Augment the original comments dataframe with the annotation labels.
comments['attack'] = labels_attack
comments['recipient_attack'] = labels_recipient_attack
comments['third_party_attack'] = labels_third_party_attack

print(f"No of attacks: {len(comments.query('attack'))}")
print(f"No of recipient attacks: {len(comments.query('recipient_attack'))}")
print(f"No of third-party attacks: {len(comments.query('third_party_attack'))}")

# Reinsert the newlines and tabs.
comments['comment'] = comments['comment'].apply(lambda x: x.replace("NEWLINE_TOKEN", "\n"))
comments['comment'] = comments['comment'].apply(lambda x: x.replace("TAB_TOKEN", "\t"))

# Print a sample of the available comments for the user.
print("Sample of the personal attacks:")
print(f"\t{comments.query('attack')['comment'].head(SAMPLES_TO_SHOW)}")
print("Sample of the non-attacks:")
print(f"\t{comments.query('not(attack)')['comment'].head(SAMPLES_TO_SHOW)}")
