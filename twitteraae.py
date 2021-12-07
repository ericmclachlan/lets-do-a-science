"""
A module for interacting with the TwitterAAE library.

Author: Eric McLachlan
"""

from typing import List

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
    predictions = predict.predict(text.split())
    assert len(predictions) == len(LABELS)

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


if __name__ == "__main__":
    _test()
