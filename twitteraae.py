"""
A module for interacting with the TwitterAAE library.

Author: Eric McLachlan
"""

from typing import List

import sys
import csv
import pandas as pd
import predict


# Constants

LABELS = [
    "African-American",
    "Hispanic        ",
    "Asian           ",
    "White           "
]

# Initialization

predict.load_model()


# Methods

def predict_constituency(text: str) -> List[float]:
    """
    Makes a prediction of the consituency of the community represented by the specified text.
    """

    # Pre-conditions:
    assert text
    assert len(text) > 0

    # Get predictions for the constituents
    try:
        tokens = text.split()
        assert tokens

        predictions = predict.predict(tokens)
        if predictions is None:
            predictions = [float('NaN'), float('NaN'), float('NaN'), float('NaN')]

        assert len(predictions) == len(LABELS)
    except Exception as ex:
        print("ERROR: Unable to get prediction for:")
        print("===")
        print(text)
        print('---')
        print(str(ex))
        print('---')


    return predictions


def print_predictions(text, prediction):
    """
    Prints the specified text and the predicted constituency for the specified text.
    """
    print("===")
    print(text)
    print("---")
    for i, label in enumerate(LABELS):
        print(f"\t{label}: {str(round(prediction[i]*100, 1))}%")


def _test():
    print("Testing...")

    # Check a quote from The Color Purple:
    text = u"Folks don't like nobody being too proud, or too free."

    try:
        predictions = predict_constituency(text)

        print_predictions(text, predictions)

        print("Test successful!")

    except Exception as ex:
        print("Error: Test failure")
        if ex and len(str(ex)) > 0:
            print(f"\t{str(ex)}")
        else:
            print("\tError details unavailable.")


def add_constituents():

    # Read the corpus with annotations.
    filename = '../../corpus.with_annotations.tsv'
    df = pd.read_csv(filename, sep = '\t', index_col = 0)

    african_american = []
    hispanic = []
    asian_constituency = []
    white = []

    for comment in df['comment']:

        # Predict the constituencies.
        constituencies = predict_constituency(comment)
        assert len(constituencies) == len(LABELS)

        african_american.append(constituencies[0])
        hispanic.append(constituencies[1])
        asian_constituency.append(constituencies[2])
        white.append(constituencies[3])

    df['african_american'] = african_american
    df['hispanic'] = hispanic
    df['asian_constituency'] = asian_constituency
    df['white'] = white

    # Save the corpus with annotations and constituents.
    filename = '../../corpus.with_constituents.tsv'
    df.to_csv(filename, sep='\t', quoting=csv.QUOTE_NONNUMERIC)

    # Post-Conditions:

    # Make sure the written file equals the original dataframe.
    # read_df = pd.read_csv(filename, sep = '\t', index_col = 0)
    # print(df.compare(read_df)) # Output any differences.
    # assert df.equals(read_df)



if __name__ == "__main__":

    command: str = None
    command = 'add_constituents' # TODO: Remove this line
    if not command:
        if len(sys.argv) > 1:
            command = sys.argv[1]

    if command == 'add_constituents':
        add_constituents()

    else:
        # By default, just run a simple test.
        _test()
