import numpy as np
import pandas as pd
import jieba
from jieba import posseg as pseg
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

# mapping the scores to orders, since classification models cannot deal with the original scores
scores = [40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0]
score2ord = {scores[i]: i for i in range(len(scores))}
ord2score = {i: scores[i] for i in range(len(scores))}

def get_text_feature_from_ltp_results(text, text_dict, feature='c'):

    """
    input: 
     - text: str, the essay text
     - text_dict: dict, ltp parsing results
    return: 
     - corpus_line: str, one item in the Corpus list
    """

    if feature not in ['c', 'w', 'cw', 'wp', 'cwp']:
        print('feature not supported, please refer to: \n[char, word, char/word, wp, char/word, pos]')
        return None

    if feature == 'c':
        charlist = list(text)
        charlist = [c for c in charlist if c.strip()]
        corpus_line = ' '.join(charlist)
    elif feature == 'w':
        wordlist = []
        for k,v in text_dict.items():
            wordlist.extend(v['wordlist'])
        corpus_line = ' '.join(wordlist)
    elif feature == 'cw':
        charlist = list(text)
        charlist = [c for c in charlist if c.strip()]
        wordlist = []
        for k,v in text_dict.items():
            wordlist.extend(v['wordlist'])
        corpus_line = ' '.join(charlist) + ' ' + ' '.join(wordlist)

    elif feature == 'wp':
        wordlist, poslist = [], []
        for k,v in text_dict.items():
            wplist = v['wplist']
            for wp in wplist:
                wpl = wp.split('/')
                if len(wpl) != 2:
                    continue
                w, p = wpl[0], wpl[1]
                wordlist.append(w)
                poslist.append(p)
        corpus_line = ' '.join(wordlist) + ' ' + ' '.join(poslist)

    elif feature == 'cwp':
        charlist = list(text)
        charlist = [c for c in charlist if c.strip()]
        wordlist, poslist = [], []
        for k,v in text_dict.items():
            wplist = v['wplist']
            for wp in wplist:
                wpl = wp.split('/')
                if len(wpl) != 2:
                    continue
                w, p = wpl[0], wpl[1]
                wordlist.append(w)
                poslist.append(p)
        corpus_line = ' '.join(charlist) + ' ' + ' '.join(wordlist) + ' ' + ' '.join(poslist)

    return corpus_line


def get_text_matrix(corpus, ngram_min=1, ngram_max=1, df_threshold=20, sparse=False):
    """
    transform the corpus to tf-idf matrix
    """
    # tf-idf feature
    # token_pattern: default=r”(?u)\b\w\w+\b”
    vectorizer = CountVectorizer(ngram_range=(ngram_min, ngram_max),
                                min_df=df_threshold,
                                token_pattern='[\w，,。.！!？?；;、]+')
    tfidf_transformer = TfidfTransformer()

    corpus_counts = vectorizer.fit_transform(corpus)
    corpus_mat = tfidf_transformer.fit_transform(corpus_counts)
    if sparse:
        corpus_mat = corpus_mat.toarray()
    print(f'Creating Tf-Idf matrix of shape {corpus_mat.shape}.')

    return corpus_mat
