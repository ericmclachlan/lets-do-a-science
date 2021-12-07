"""
A module for testing the readability of the Wikipedia Talk Corpus: Personal Attack corpus.

Heavily inspired by a Jupyter notebook template provided here:
    https://github.com/ewulczyn/wiki-detox/blob/master/src/figshare/Wikipedia%20Talk%20Data%20-%20Getting%20Started.ipynb

"""

import csv
import sys
import pandas as pd

# Constants

ATTACK_ANNOTATIONS_FILE = "attack_annotations.tsv"
ATTACK_ANNOTATED_COMMENTS_FILE = "attack_annotated_comments.tsv"
SAMPLES_TO_SHOW=3


def load_corpus() -> pd.DataFrame:

    # Loads the comments and annotations files.
    print("Wikipedia Talk Labels: Personal Attacks: Loading...")
    df = pd.read_csv('attack_annotated_comments.tsv', sep = '\t', index_col = 0)
    annotations = pd.read_csv('attack_annotations.tsv',  sep = '\t')

    # print(len(comments['rev_id'].unique()))
    print(f"No of comments annotated: {len(annotations['rev_id'].unique())}")

    # Annotations by majority voting.
    labels_attack = annotations.groupby('rev_id')['attack'].mean() > 0.5
    labels_recipient_attack = annotations.groupby('rev_id')['recipient_attack'].mean() > 0.5
    labels_third_party_attack = annotations.groupby('rev_id')['third_party_attack'].mean() > 0.5

    # Augment the original comments dataframe with the annotation labels.
    df['attack'] = labels_attack
    df['recipient_attack'] = labels_recipient_attack
    df['third_party_attack'] = labels_third_party_attack

    print(f"No of attacks: {len(df.query('attack'))}")
    print(f"No of recipient attacks: {len(df.query('recipient_attack'))}")
    print(f"No of third-party attacks: {len(df.query('third_party_attack'))}")

    # Reinsert the newlines and tabs.
    df['comment'] = df['comment'].apply(lambda x: x.replace("NEWLINE_TOKEN", "\n"))
    df['comment'] = df['comment'].apply(lambda x: x.replace("TAB_TOKEN", "\t"))

    return df


def _test():
    df = load_corpus()

    # Print a sample of the available comments for the user.
    print("Sample of the personal attacks:")
    print(f"\t{df.query('attack')['comment'].head(SAMPLES_TO_SHOW)}")
    print("Sample of the non-attacks:")
    print(f"\t{df.query('not(attack)')['comment'].head(SAMPLES_TO_SHOW)}")


# Run a simple test.
if __name__ == "__main__":

    command: str = None
    command = 'add_annotations' # TODO: Remove this line
    if not command:
        if len(sys.argv) > 1:
            command = sys.argv[1]

    if command == 'add_annotations':
        df = load_corpus()

        # Save the corpus with annotations to a file.
        filename = 'corpus.with_annotations.tsv'
        df.to_csv(filename, sep='\t', quoting=csv.QUOTE_NONNUMERIC)

        # Post-Conditions:

        # Make sure the written file equals the original dataframe.
        read_df = pd.read_csv(filename, sep = '\t', index_col = 0)
        assert df.equals(read_df)

    else:
        # By default, just run a simple test.
        _test()
