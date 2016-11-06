import re

import pandas as pd


EMOJIS = pd.read_csv('data/emojis.txt', header=None)[0].tolist()

SPAMMY_PATTERNS = [
    'bbm|pin bb|line|whatsapp',
    '(ch?ec?k|intip|liat|kepoin)( out)?( (our|my))? (ig|insta|koleksi|profil)',
    'cekidot',
    'dada|herba|langsing|payudara|pemutih|penggemuk|peninggi|tahan lama|tinggi badan',
    'efek samping',
    'follow',
    'free (delivery|ongkos|ongkir|pengiriman)|gratis|murah|promo|terjangkau',
    'garansi|kualitas',
    'impor',
    'invit',
    'jerawat',
    'jual|sell',
    'langganan',
    'luar biasa',
    'mampir',
    'nyaranin',
    'order',
    'password',
    'penghasilan',
    'produk',
    's(o|u|ou)venir',
    'stock|stok',
    'yu+k',
]


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

def extract_emojis(texts):
    # type: (pd.Series) -> pd.Series
    """ Return all emojis contained in each text in texts """
    return texts.apply(lambda x: [c for c in x if c in EMOJIS])

def extract_spammy_pattern_features(texts):
    # type: (pd.Series) -> pd.DataFrame
    """ Return a DataFrame for each pattern in SPAMMY_PATTERNS,
    denoting whether each text in text contains the pattern """
    spammy_pattern_features = {
        'has_pattern_{}'.format(pat): texts.str.contains(pat.replace(' +', '\s+'), case=False)
        for pat in SPAMMY_PATTERNS
    }
    spammy_pattern_features = pd.DataFrame(spammy_pattern_features)
    spammy_pattern_features.index = texts.index
    return spammy_pattern_features

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


def extract_features(X):
    X = X.copy()    # don't modify the input dataset

    X['text'] = X['text'].str.strip()
    X['tokens'] = tokenize_2(X['text'])
    X['text_clean'] = X['tokens'].apply(' '.join)
    X['emojis'] = extract_emojis(X['text'])

    X['n_char'] = X['text'].str.len()
    X['n_token'] = X['tokens'].apply(len)
    X['n_capital'] = count_capitals(X['text'])
    X['n_number'] = count_numbers(X['text'])
    X['n_emoji'] = X['emojis'].apply(len)
    X['n_unique_emoji'] = X['emojis'].apply(set).apply(len)

    X['%_capital'] = X['n_capital'] / X['n_char']
    X['%_number'] = X['n_number'] / X['n_char']
    X['%_emoji'] = X['n_emoji'] / X['n_char']
    X['%_unique_emoji'] = X['n_unique_emoji'] / X['n_char']

    X = pd.concat([X, extract_spammy_pattern_features(X['text'])], axis=1)
    return X
