# lets-do-a-science

Author: Eric McLachlan

This work was done as the term project for a masters course titled "Societal Impacts of NLP" offered as part of the Computational Linguistics Masters of Science through the University of Washington.

## Installation

To install the necessary software, run:

```sh
python -m pip install -r requirements.txt
```

Add your Perspective API key to the environment:

```sh
export PERSPECTIVE_API_KEY="Replace this with your Perspective API key"
```

## Resources

### TwitterAAE - Blodget et al (2016)

This project leans relies on the work done by Su Lin Blodgett, Lisa Green, and Brendan O'Connor, EMNLP 2016.

Thanks to all of them for making their work available to the community.

Their original classifier can be found here:
https://github.com/slanglab/twitteraae

The paper related to the classifier can be found here:

> @inproceedings{blodgett2016demographic,
author = {Blodgett, Su Lin and Green, Lisa and O'Connor, Brendan},
title = {{Demographic Dialectal Variation in Social Media: A Case Study of African-American English}},
booktitle = {Proceedings of EMNLP},
year = 2016}

### Wikipedia Talk Corpus: Personal Attack

According to their [website](https://figshare.com/articles/dataset/Wikipedia_Talk_Labels_Personal_Attacks/4054689?file=7554637),

```
This data set includes over 100k labeled discussion comments from English Wikipedia. Each comment was labeled by multiple annotators via Crowdflower on whether it contains a personal attack.
```

**DOI**: https://doi.org/10.6084/m9.figshare.4054689.v6

**Wiki**: https://meta.wikimedia.org/wiki/Research:Detox/Data_Release

**Citation**:

> Wulczyn, Ellery; Thain, Nithum; Dixon, Lucas (2017): Wikipedia Talk Labels: Personal Attacks. figshare. Dataset. https://doi.org/10.6084/m9.figshare.4054689.v6
