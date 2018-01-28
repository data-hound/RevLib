import pandas as pd
import json

import numpy as np
#import math

#import matplotlib
import matplotlib.pyplot as plt

from pandas import DataFrame
import seaborn as sns; sns.set(style="ticks", color_codes=True)


#import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

def read_data(filename):
    #with open(filename) as train_file:
    #    dict_train = json.load(train_file)

    #df = pd.DataFrame.from_dict(dict_train, orient='index')
    df = pd.read_json(filename, orient = "columns", typ ="frame")
    #df = pd.read_csv(filename)
    return df

def SentAnalyse(filename):
    df = read_data(filename)

    content = []
    text = []
    rating = []
    title = []
    for idx,row in df.iterrows():
        #print row
        words = row[-1]
        review_title = words[0]
        review_text = words[1]
        review_rating = words[2]
        content.append(words)
        text.append(review_text)
        rating.append(review_rating)
        title.append(review_title)
        print review_text, review_rating
    #print content
    #print text
    #print df

    sid = SentimentIntensityAnalyzer()
    #text = df[df.columns[-1]]
    comments = []
    #sen_score=[]
    neg_score = []
    pos_score = []
    neutral_score = []
    compound_score = []

    for i in range(len(text)):
        comment = title[i]+" "+text[i]
        comments.append(comment)
        bhawnaye = sid.polarity_scores(title[i]+" "+text[i])
        #sen_score.append(sorted(bhawnaye))
        neg_score.append(bhawnaye['neg'])
        pos_score.append(bhawnaye['pos'])
        neutral_score.append(bhawnaye['neu'])
        compound_score.append(bhawnaye['compound'])
        #print i
        #print bhawnaye
    #print comments

    nf = DataFrame(
        {
            "title":title,
            "text":text,
        }
    )

    nf["rating"] = pd.Series(rating)
    nf["Pos Score"] = pd.Series(pos_score)
    nf["Neg Score"] = pd.Series(neg_score)
    nf["Neutral Score"] = pd.Series(neutral_score)
    nf["Compound Score"] = pd.Series(compound_score)

    nf.to_csv("New_"+filename[:-5]+".csv")
    nf.to_json("New_"+filename, orient = "split")
    #df.to_csv("New_"+filename)

#SentAnalyse('try_1_3_2_final.json')
SentAnalyse('Apple_iPhone_7_128GB.json')
