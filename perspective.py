"""
A file for accessing Google's Perspective API.
    https://developers.perspectiveapi.com/s/docs-sample-requests
"""

import csv
import math
import os
import shutil
import sys
import time

import pandas as pd

from googleapiclient import discovery
from googleapiclient.errors import HttpError
from pandas.core.frame import DataFrame


# Constants

API_KEY = os.getenv('PERSPECTIVE_API_KEY')
DISCOVERY_SERVICE_URL = "https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1"
FEEDBACK_RATIO = 10  # Print user feedback every X texts.
WITH_CONSTITUENTS_FILENAME = 'corpus.with_constituents.tsv'
WITH_PERSPECTIVE_FILENAME = 'corpus.with_perspective.tsv'

# Methods

def predict_insult(text: str):
    """
    Sends a prediction request for the specified text to the Perspective API.
    """

    # Keep retrying until, either:
    # a) we succeeed, or
    # b) there is an error unrelated to a timeout.
    while True:
        try:
            client = discovery.build(
                "commentanalyzer",
                "v1alpha1",
                developerKey=API_KEY,
                discoveryServiceUrl=DISCOVERY_SERVICE_URL,
                static_discovery=False,
            )

            analyze_request = {
                'comment': { 'text': text},
                'requestedAttributes': {'INSULT': {}},
                'languages': ['en'],
                'doNotStore': True
            }

            response = client.comments().analyze(body=analyze_request).execute()

            prediction = response['attributeScores']['INSULT']['summaryScore']['value']

            # Post-conditions
            assert isinstance(prediction, float)

            return prediction

        except HttpError as ex:
            print("WARNING: Error using the Perspective API to predict:")
            # print_prediction(text, None)
            msg = repr(ex)
            print(f"Error details: {msg}")
            time.sleep(1)  # Give the API a little time to catch up.
            print("Retrying...")
            # continue to the next iteration of the infinite while loop.

        except Exception as ex:
            print("ERROR: Error using the Perspective API to predict:")
            print_prediction(text, None)
            print(f"Error details: {str(ex)}")
            return float('NaN')


def print_prediction(text: str, prediction: float):
    """
    Displays some feedback about the prediction to the user.
    """

    # Print some user feedback:
    print('===')
    print(text)
    # print('---')
    # print(json.dumps(response, indent=2))
    print('---')
    if prediction is None:
        print('Insult: null')
    else:
        print(f'Insult: {prediction*100.0:.2f}%')


def add_perspective():
    """
    Addds predictions received from the Perspective API to the dataframe and stores
    the resulting data in a file.
    """

    if os.path.isfile(WITH_PERSPECTIVE_FILENAME):
        # We may have partial results, in which case continue where we left off.
        df = _load(WITH_PERSPECTIVE_FILENAME)
    else:
        assert os.path.isfile(WITH_CONSTITUENTS_FILENAME)

        # Read the corpus with annotations.
        df = _load(WITH_CONSTITUENTS_FILENAME)

        # Add this column to the data frame
        df['perspective'] = [None] * len(df['comment'])
        _save(WITH_PERSPECTIVE_FILENAME, df)

    # Generate predictions:
    samples_processed = 0
    for row in df.itertuples(index=True):

        if row.perspective is None or math.isnan(row.perspective):

            samples_processed += 1 # Increase the counter.

            # Generate a prediction
            start = time.time()
            prediction = predict_insult(row.comment)
            df.at[row.Index, 'perspective'] = prediction

            print_prediction(row.comment, prediction)

            if samples_processed > 60:
                _save('tmp.tsv', df)  # Save the file.
                shutil.copy('tmp.tsv', WITH_PERSPECTIVE_FILENAME)  # Replace the file containing the perspective.
                samples_processed = 0

            # Throttle the rate of requests to one request per second.
            duration = time.time() - start
            if duration < 1.0:
                time.sleep(1 - duration) # Wait until a full second has passed.

    # Save the last few samples since the last checkpoint.
    _save('tmp.tsv', df)  # Save the file.
    shutil.copy('tmp.tsv', WITH_PERSPECTIVE_FILENAME)  # Replace the file containing the perspective.


# Private Methods

def _load(filename: str) -> pd.DataFrame:
    assert filename
    df = pd.read_csv(filename, sep = '\t', index_col = 'rev_id')
    assert df is not None
    return df

def _save(filename: str, df: pd.DataFrame):

    # Pre-conditions
    assert filename
    assert df is not None
    assert isinstance(df, DataFrame)

    # Save the file.
    df.to_csv(filename, sep='\t', quoting=csv.QUOTE_NONNUMERIC)


def _test():
    text = "This is a totally benign statement."
    prediction = predict_insult(text)
    print(f"Prediction: {prediction}")


if __name__ == "__main__":

    command: str = None
    command = 'add_perspective' # TODO: Remove this line
    if not command:
        if len(sys.argv) > 1:
            command = sys.argv[1]

    if command == 'add_perspective':
        add_perspective()

    else:
        # By default, just run a simple test.
        _test()
