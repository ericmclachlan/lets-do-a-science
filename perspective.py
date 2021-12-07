"""
A file for accessing Google's Perspective API.
    https://developers.perspectiveapi.com/s/docs-sample-requests
"""

import os
import sys

from googleapiclient import discovery


# Constants

API_KEY = os.getenv('PERSPECTIVE_API_KEY')


# Methods

def PredictInsult(text: str):
    """
    Sends a prediction request for the specified text to the Perspective API.
    """

    client = discovery.build(
      "commentanalyzer",
      "v1alpha1",
      developerKey=API_KEY,
      discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
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
    assert 'en' in response['detectedLanguages']

    # Print some user feedback:
    print('===')
    print(text)
    # print('---')
    # print(json.dumps(response, indent=2))
    print('---')
    print(f'Prediction: {prediction*100.0:.2f}%')

    # Return the prediction to the caller.
    return prediction


def add_perspective():
    print("TODO: Use the Perspective API to predict insults.")


def _test():
    text = "This is a totally benign statement."
    prediction = PredictInsult(text)
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
