import pandas as pd
from autocorrect import spell
import re
import nltk
from nltk import word_tokenize


addv = {'vp':'vice president', 'hr': 'human resouce', 'r d': 'research'
            'qa': 'qa', 'qc':'qc', 'mgr':'manager', 'ceo':'ceo',
        }

PATTERN_1 = ["sales", "accounts", "business"]
PATTERN_2 = ["accounting", "finance"]


def remove_special_character(str):
    return(re.sub('[^A-Za-z]+', ' ',str))

def preprocessing(path = "Sample_data.csv"):
    df = pd.read_csv(path)
    title = [remove_special_character(str(s)).lower().strip() for s in df['Title']]
    df['Title'] = title
    df = df.drop(['Function', 'Level'], axis = 1)
    return(df)

def process2word(title):
    title = [spell(w) for w in word_tokenize(title)]
    w1 = title[0]
    w2 = title[1]
    function = ""
    level = ""
    if (w1 in PATTERN_1):
        function = "sales"
        level = w2
    elif (w1 in PATTERN_2):
        function = "finance"
        level = w2
    else:
        function = w1
        level = w2
    return (function, level)

def get_unique(df):
    uni_title = set(list(df['Title']))
    dct = {}
    for title in uni_title:
        if len(title.split(' ')) == 1:
            dct[title] = (title, "")
        if len(title.split(' ')) == 2:
            dct[title] = process2word(title)
