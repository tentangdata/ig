import re

import pandas as pd


EMOJIS = pd.read_csv('data/emojis.txt', header=None)[0].tolist()


def count_numbers(texts):
    # type: (pd.Series) -> pd.Series
    """ Return number of digits for each text in texts """
    return texts.apply(lambda x: sum(c.isdigit() for c in x))

def count_capitals(texts):
    # type: (pd.Series) -> pd.Series
    """ Return number of capital letters for each text in texts """
    return texts.apply(lambda x: sum(c.isupper() for c in x))

def count_emojis(texts):
    # type: (pd.Series) -> pd.Series
    """ Return number of emojis for each text in texts """
    return texts.apply(lambda x: sum(c in EMOJIS for c in x))

def tokenize(texts):
    # type: (pd.Series) -> pd.Series
    """ Return tokenization (as list of str) of each text in texts """
    return texts.apply(lambda x: re.findall(r'\b\w+\b', x.lower()))

def tokenize_2(texts):
    # type: (pd.Series) -> pd.Series
    """ Return tokenization (as list of str) of each text in texts.
        Use a different regex than tokenize()
    """
    re_tokenize = re.compile('[!"#$%&\'()*+,./:;<=>?@\[\]^_{|}~\s-]')
    return texts\
        .apply(re_tokenize.split)\
        .apply(lambda x: [tok for tok in x if tok])    # remove empty tokens

def _flatten(L):
    return [item for sublist in L for item in sublist]


def _get_emoji_list(fpath_emoji_webpage='data/Full Emoji Data, v3.0.html'):
    from bs4 import BeautifulSoup

    with open(fpath_emoji_webpage) as f:
        soup = BeautifulSoup(f.read(), 'lxml')

    rows = soup.table.find_all('tr')
    rows = [row for row in rows if row.find('td', attrs={'class': 'code'})]

    emojis = sorted(set(_flatten([row.find('td', attrs={'class': 'chars'}).text.strip().split() for row in rows])))
    return emojis
