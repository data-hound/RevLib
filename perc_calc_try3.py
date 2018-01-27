import pandas as pd
from gensim.models import Word2Vec
#https://codesachin.wordpress.com/2015/10/09/generating-a-word2vec-model-from-a-block-of-text-using-gensim-python/
#http://nadbordrozd.github.io/blog/2016/05/20/text-classification-with-word2vec/
#references for the word2vec model
# the second reference provides an alternative of using Glove pretrained vectors(https://nlp.stanford.edu/projects/glove/)

#import numpy as np
#import math

#import matplotlib
import matplotlib.pyplot as plt

from pandas import DataFrame
import seaborn as sns; sns.set(style="ticks", color_codes=True)


import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
sid = SentimentIntensityAnalyzer()
noun_scores = dict()

def pentagram(tagged, adj, noun_scores):
    #pos_noun_scores = nltk.defaultdict(int)
    #neg_noun_scores = nltk.defaultdict(int)
    #neu_noun_scores = nltk.defaultdict(int)
    #print adj
    #print tagged
    for adj_type in adj:
        for i in adj_type:
            #print i
            pos = i[1]
            low_end_phrase = pos-2 if pos-2 >= 0 else 0
            high_end_phrase = pos+2 if pos+2 <len(tagged) else len(tagged)-1
            phrase = []
            sent_score = sid.polarity_scores(i[0])
            for i in range(low_end_phrase,high_end_phrase+1):
                if tagged[i][1] == "NN" or tagged[i][1] == "NNs":
                    # We collect all the common nouns in the vicinity of the adjectives
                    noun = tagged[i][0]
                    if sent_score["compound"] > 0:
                        if noun in noun_scores:
                            noun_scores[noun][0] +=1
                        else:
                            noun_scores[noun] = [1,0]
                    if sent_score["compound"] < 0:
                        if noun in noun_scores:
                            noun_scores[noun][1] +=1
                        else:
                            noun_scores[noun] = [0,1]

    #print noun_scores
    #return noun_scores

def read_data(filename):
    df = pd.read_csv ("New_"+filename)
    return df

def calc_perc(filename, noun_scores):
    df = read_data(filename)
    text = df[df.columns[2]]
    corp = ""
    #sen_score=[]
    neg_score = []
    pos_score = []
    neutral_score = []
    compound_score = []

    for idx,row in df.iterrows():
        review = row["text"] + " " + row["title"]
        review = review.strip().lower()
        corp += review
        u_rating = row["rating"]
        pred_score = row["Compound Score"]
        tokenized_rev = nltk.word_tokenize(review)
        tagged = nltk.pos_tag(tokenized_rev)

        pos_dict = dict()
        pos_dict["NN"] = []

        for i in range(len(tagged)):
            word,tag = tagged[i]
            if tag in pos_dict:
                pos_dict[tag].append((word,i))
            else:
                pos_dict[tag] = [(word,i)]

        adj = []


        try :
            adj.append(pos_dict["JJ"])
            #print "Numeral or ordinal adjectives: ",pos_dict["JJ"]
        except:
            #print "No numeral Adjective or ordinal"
            print

        try :
            adj.append(pos_dict["JJR"])
            #print "Numeral or comparative adjectives: ",pos_dict["JJR"]
        except:
            #print "No comparative Adjectives"
            print


        try :
            adj.append(pos_dict["JJS"])
            #print "Numeral or subjective adjectives: ",pos_dict["JJS"]

        except:
            #print "No subjective Adjectives"
            print


        pentagram(tagged, adj, noun_scores)

    print noun_scores
    #print corp
    return corp
    #df.to_csv("New_"+filename)

def get_scores(filename, noun_scores):
    corp = calc_perc(filename, noun_scores)
    #keyFeaturesList = ["product","screen","camera","memory","size","battery","weight","technology"]
    keyFeaturesList = ["phone","screen","camera","memory","battery","shipping"]
    feature_maps = {}
    feature_maps["phone"]  = ["iphone", "smartphone", "mobile", "product","device","handset"]
    feature_maps["screen"] = ["display","touch","size","glass"]
    feature_maps["camera"] = ["cam"]
    feature_maps["memory"] = ["storage"]
    feature_maps["battery"] = ["power","backup","standby"]
    feature_maps["shipping"] = ["delivery"]
    #print corp
    tokens = nltk.word_tokenize(corp)
    text = nltk.Text(tokens)

    pref_scores = {}
    pref_scores["phone"] = [0,0]
    pref_scores["screen"] = [0,0]
    pref_scores["camera"] = [0,0]
    pref_scores["memory"] = [0,0]
    pref_scores["battery"] = [0,0]
    pref_scores["shipping"] =[0,0]

    '''
    #training our own word2vec on the text
    min_counts = 5                          # terms that occur less than min_count number of times are ignored from computations
    size = 100                             # the dimensionality of vectors
    window = 20                             # Only terms hat occur within a window-neighbourhood of a term, in a sentence, are associated with it during training
    model = Word2Vec([tokens], min_count=min_counts, size=size, window=window)
    '''

    #print text
    for feature in keyFeaturesList:
        print feature,":"
        for sim_features in feature_maps[feature]:
            try :
                pref_scores[feature][0] += noun_scores[sim_features][0]
                pref_scores[feature][0] += noun_scores[feature][0]
                pref_scores[feature][1] += noun_scores[sim_features][1]
                pref_scores[feature][1] += noun_scores[feature][1]
            except:
                print "Failing Silently"

    print pref_scores


get_scores('IphoneX_Amazon_Reviews.csv', noun_scores)
