"""
A module for running our experiments.

Author: Eric McLachlan
"""

import predict

LABELS = [
    "African-American",
    "Hispanic        ",
    "Asian           ",
    "White           "
]

predict.load_model()

# Check a quote from The Color Purple:
samples = [
    u"Folks don't like nobody being too proud, or too free.",
]
for sample in samples:
    try:
        print(sample)
        # Run each sample through the classifier.
        prediction = predict.predict(sample.split())
        assert(len(prediction) == len(LABELS))
        (african_american, hispanic, asian, white) = prediction
        for i, label in enumerate(LABELS):
            print(f"\t{label}: {str(round(prediction[i]*100, 1))}%")
        print("Test successful!")
    except Exception as ex:
        print("Error: Test failure")
        if ex and len(str(ex)) > 0:
            print(f"\t{str(ex)}")
        else:
            print(f"\tError details unavailable.")