import pandas as pd

#import numpy as np
#import math

#import matplotlib
import matplotlib.pyplot as plt

from pandas import DataFrame
import seaborn as sns; sns.set(style="ticks", color_codes=True)


import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize


def read_data(filename):
    df = pd.read_csv ("New_"+filename)
    return df

def get_corp(filename):
    df = read_data(filename)
    text = df[df.columns[2]]
    corp = ""

    for idx,row in df.iterrows():
        review = row["text"] + " " + row["title"]
        review = review.strip().lower()
        corp += review

    #print noun_scores
    #print corp
    return corp,df
    #df.to_csv("New_"+filename)

def get_least_freq(filename):
    corp,df = get_corp(filename)
    tokens = nltk.word_tokenize(corp)
    text = nltk.Text(tokens)

    fdist = nltk.FreqDist(text)
    all_words = fdist.keys()
    most_informative = all_words[-200:]
    #print most_informative

    info_score = []
    max_info = 0

    for idx,row in df.iterrows():
        review = row["text"] + " " + row["title"]
        review = review.strip().lower()
        tokenized_rev = nltk.word_tokenize(review)
        tokenized_rev = set(tokenized_rev)

        info_words_in_rev = tokenized_rev.intersection(most_informative)
        abs_info_score = len(info_words_in_rev)

        info_score.append(abs_info_score)

        if abs_info_score >= max_info:
            max_info = abs_info_score

    for i in range(len(info_score)):
        info_score[i] = info_score[i]/float(max_info)
        #print info_score[i]

    df["Info_score"] = info_score
    df = df[df.columns[-8:]]
    df.to_csv("New_"+filename)



    return most_informative

get_least_freq('IphoneX_Amazon_Reviews.csv')
