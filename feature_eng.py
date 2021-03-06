import fasttext
import gensim
import numpy as np
import pandas as pd
import re


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

def extract_word_embedding(tokens):
    # type: (pd.Series) -> pd.DataFrame
    """ Return a DataFrame for 100-dimension word embedding """
    word_embedding = pd.DataFrame(_get_w2v_mean(tokens).tolist(), columns=['embedding_{}'.format(i) for i in range(100)])
    word_embedding.index = tokens.index
    return word_embedding

def _get_w2v_mean(tokens, fpath_model='data/classification.model'):
    model = gensim.models.Word2Vec.load(fpath_model)
    return tokens.apply(lambda x: _get_mean(x, model))

def extract_fasttext(texts, fpath_model='/tmp/model.bin'):
    # type: (pd.Series) -> pd.DataFrame
    """ Return a DataFrame for 100-dimension word embedding """
    tokens = tokenize(texts)
    embedding = pd.DataFrame(_get_fasttext_mean(tokens, fpath_model=fpath_model).tolist(),
                             columns=['embedding_{}'.format(i) for i in range(100)])
    embedding.index = texts.index
    return embedding

def train_model_fasttext(tokens, file_in='data/train.txt', path_out='/tmp/model'):
    tokens.apply(' '.join).to_csv(file_in, index=False) # writing to .txt file
    model = fasttext.skipgram(file_in, path_out)
    return model

def _get_fasttext_mean(tokens, fpath_model='/tmp/model.bin'):
    model = fasttext.load_model(fpath_model)
    return tokens.apply(lambda x: _get_mean(x, model))

def _get_mean(tokens, model):
    i = 0
    total = np.zeros(100)
    for token in tokens:
        if token in model:
            total += model[token]
            i += 1
    return total / i if i != 0 else total

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
    # X['text_clean'] = X['tokens'].apply(' '.join)
    X['emojis'] = extract_emojis(X['text'])

    X['n_char'] = X['text'].str.len()
    X['n_token'] = X['tokens'].apply(len)
    X['n_capital'] = count_capitals(X['text'])
    X['n_number'] = count_numbers(X['text'])
    X['n_emoji'] = X['emojis'].apply(len)
    X['n_unique_emoji'] = X['emojis'].apply(set).apply(len)
    X['n_mention'] = X['text'].str.count('@')

    X['%_capital'] = X['n_capital'] / X['n_char']
    X['%_number'] = X['n_number'] / X['n_char']
    X['%_emoji'] = X['n_emoji'] / X['n_char']
    X['%_unique_emoji'] = X['n_unique_emoji'] / X['n_char']

    X['log_char'] = X['n_char'].apply(np.log)

    X['has_phone_number'] = X['text'].str.contains('(\d[ \.-]?){9}')
    X['has_bbm_pin'] = X['text'].str.contains('([0-9][A-F0-9]{7})|([A-F0-9][0-9][A-F0-9]{6})|([A-F0-9]{2}[0-9][A-F0-9]{5})|([A-F0-9]{3}[0-9][A-F0-9]{4})|([A-F0-9]{4}[0-9][A-F0-9]{3})|([A-F0-9]{5}[0-9][A-F0-9]{2})|([A-F0-9]{6}[0-9][A-F0-9])|([A-F0-9]{7}[0-9])', case=False)

    # X = pd.concat([X, extract_word_embedding(X['tokens'])], axis=1)

    X = pd.concat([X, extract_spammy_pattern_features(X['text'])], axis=1)
    return X

def test():
    train = pd.read_pickle('data/train.p')
    validate = pd.read_pickle('data/validate.p')
    test = pd.read_pickle('data/test.p')
    train_model_fasttext(tokenize(train.text))

if __name__ == '__main__':
    test()