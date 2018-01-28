import pandas as pd
import json
import os
import math
import numpy as np
#import math

#import matplotlib
#import matplotlib.pyplot as plt

from pandas import DataFrame
#import seaborn as sns; sns.set(style="ticks", color_codes=True)

"""
If you use the VADER sentiment analysis tools, please cite:

Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for
Sentiment Analysis of Social Media Text. Eighth International Conference on
Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
"""


import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

sid = SentimentIntensityAnalyzer()
noun_scores = dict()

'''def CleanByDrop(filename):
    df = pd.read_json(filename, orient = "columns", typ ="frame")
    #print df.iloc[0][1]
    #print df[df.columns[0]]
    #print list(df.columns.values)

    df2 = pd.read_json(filename, orient = "index", typ = "frame")
    #print "df2"
    #print df2.iloc[0]
    print df2[df2.columns[0]]
    #print list(df2.columns.values)

    with open(filename, 'r') as f:
        out_list = json.load(f)
    print type(out_list[0])

    count = 0

    for i in out_list:
        if len(i.values()[0].items())<17:
            out_list.remove(i)
            print "REMOVING ITEM............."
            print i
            print "num_values=",len(i.values()[0].items())
            count += 1

    flag=0
    print "Counts = ",count
    print "============================================================"

    for i in out_list:
        if len(i.values()[0].items())<17:
            print i.keys()
        print nltk.edit_distance(i.keys()[0],"phone")


    print len(out_list)'''


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
    #with open(filename) as train_file:
    #    dict_train = json.load(train_file)

    #df = pd.DataFrame.from_dict(dict_train, orient='index')
    df = pd.read_json(filename, orient = "columns", typ ="frame")
    #print "no. of columns = ", (df.iloc[0].size)," ", df.iloc[0]
    #print df

    #df = pd.read_csv(filename)
    return df

def SentAnalyse(filename, noun_scores, min_len, max_len, avg_num_rev):
    df = read_data(filename)
    content = []
    text = []
    rating = []
    title = []
    corp = ""
    num_rev = df.shape[0]

    #Opinion Mining and data list building. Any mismatch in columns can be treated here
    for idx,row in df.iterrows():
        #print "row:",row
        words = row[0]#row[-1]
        #print "words:", words
        review_title = words["title"]
        review_text = words["text"]
        review_rating = words["rating"]
        review = review_title + " " +review_text
        corp += review
        content.append(words)
        text.append(review_text)
        rating.append(review_rating)
        title.append(review_title)
        #print review_text, review_rating

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
            dummy=0

        try :
            adj.append(pos_dict["JJR"])
            #print "Numeral or comparative adjectives: ",pos_dict["JJR"]
        except:
            #print "No comparative Adjectives"
            dummy=0


        try :
            adj.append(pos_dict["JJS"])
            #print "Numeral or subjective adjectives: ",pos_dict["JJS"]

        except:
            #print "No subjective Adjectives"
            dummy=0


        pentagram(tagged, adj, noun_scores)
    #print content
    #print text
    #print df

    #text = df[df.columns[-1]]
    comments = []
    #sen_score=[]
    neg_score = []
    pos_score = []
    neutral_score = []
    compound_score = []
    num_revs = len(text)
    sum_ur = 0.0
    sum_comp_score = 0.0
    sum_cumul_score = 0.0
    cumulative_score = []

    #Sentiment Scores
    for i in range(num_revs):
        comment = title[i]+" "+text[i]
        comments.append(comment)
        bhawnaye = sid.polarity_scores(title[i]+" "+text[i])
        #sen_score.append(sorted(bhawnaye))
        neg_score.append(bhawnaye['neg'])
        pos_score.append(bhawnaye['pos'])
        neutral_score.append(bhawnaye['neu'])
        compound_score.append(bhawnaye['compound'])
        u_rating = rating[i]
        sum_ur += u_rating
        sum_comp_score += bhawnaye["compound"]

        norm_ur = (u_rating - 3.0)*2.0
        comp_score = bhawnaye["compound"]*2.0
        cumul_score = 0.0

        if (norm_ur*comp_score < 0):
            cumul_score = (norm_ur*1.5 + comp_score)/6.0
        else:
            cumul_score = (norm_ur + comp_score)/4.0

        cumulative_score.append(cumul_score)
        sum_cumul_score += cumul_score

        #print i
        #print bhawnaye
    #print comments

    avg_ur = sum_ur / num_rev
    avg_comp_score = sum_comp_score/num_rev
    avg_cumul_score = sum_cumul_score/num_rev

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
    nf["Cumulative Score"] = pd.Series(cumulative_score)

    #nf.to_csv("New_"+filename[:-5]+".csv")
    #nf.to_json("New_"+filename, orient = "split")
    #df.to_csv("New_"+filename)
    return nf, corp, avg_ur, avg_comp_score, avg_cumul_score

#SentAnalyse('try_1_3_2_final.json')
#SentAnalyse('Apple_iPhone_7_128GB.json')

def get_scores(corp, noun_scores):
    #corp = calc_perc(filename, noun_scores)
    #keyFeaturesList = ["product","screen","camera","memory","size","battery","weight","technology"]
    keyFeaturesList = ["screen","camera","memory","battery","shipping"]
    feature_maps = {}
    #feature_maps["phone"]  = ["iphone", "smartphone", "mobile", "product","device","handset"]
    feature_maps["screen"] = ["display","touch","size","glass"]
    feature_maps["camera"] = ["cam"]
    feature_maps["memory"] = ["storage"]
    feature_maps["battery"] = ["power","backup","standby"]
    feature_maps["shipping"] = ["delivery"]
    #print corp
    tokens = nltk.word_tokenize(corp)
    text = nltk.Text(tokens)

    pref_scores = {}
    #pref_scores["phone"] = [0,0]
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
        #print feature,":"
        for sim_features in feature_maps[feature]:
            try :
                pref_scores[feature][0] += noun_scores[sim_features][0]
                pref_scores[feature][0] += noun_scores[feature][0]
                pref_scores[feature][1] += noun_scores[sim_features][1]
                pref_scores[feature][1] += noun_scores[feature][1]
            except:
                dummy=0

    #print pref_scores
    return pref_scores

def main_fun(noun_scores):
    cwd = os.getcwd()
    data_dir = cwd + "/Data/"
    min_len = 100000
    max_len = 0
    sum_len = 0
    num_products = 0

    out_dir = data_dir + "/output/"

    #cleaned_out = CleanByDrop(out_dir+"out-1.json")

    with open(out_dir + "out-1.json", 'r') as f:
        out_list = json.load(f)

    print "Cleaned out.json"

    #Obtaining the total number of reviews for each product across products

    for filename in os.listdir(data_dir):
        print filename
        if filename.endswith(".json"):
            new_frame = read_data(os.path.join(data_dir,filename))
            nf_len = new_frame.shape[0]
            sum_len+=nf_len

            num_products+=1

            if (nf_len > max_len):
                max_len = nf_len
            elif (nf_len < min_len):
                min_len = nf_len

    avg_num_rev = float(sum_len)/num_products

    #updating database
    for filename in os.listdir(data_dir):
        print filename
        print "Updating Database"
        if filename.endswith(".json"):
            new_frame, corp, avg_ur, avg_comp_score, avg_cumul_score = SentAnalyse(os.path.join(data_dir,filename),noun_scores,min_len,max_len, avg_num_rev)
            pref_scores = get_scores(corp, noun_scores)

            nf_len = new_frame.shape[0]

            net_pos = 0
            net_neg = 0

            for key,value in pref_scores.iteritems():
                net_pos+=value[0]
                net_neg+=value[1]

            for key,value in pref_scores.iteritems():
                pref_scores[key][0] = float(value[0])/net_pos
                pref_scores[key][1] = float(value[1])/net_neg

            rev_theta = math.log(nf_len) - math.log(min_len) /(math.log(max_len) - math.log(min_len))

            avg_cumul_score = avg_cumul_score*rev_theta

            for i in out_list:
                print i.keys()[0].lower(), filename
                print nltk.edit_distance(i.keys()[0],filename)
                print i[i.keys()[0]]["flag"]
                if nltk.edit_distance(i.keys()[0].lower(),filename) < 20 and i[i.keys()[0]]["flag"]==-1:
                    print i[i.keys()[0]]
                    i[i.keys()[0]]["Avg. User Rating"] = avg_ur
                    i[i.keys()[0]]["Avg. Compound Score"] = avg_comp_score
                    i[i.keys()[0]]["Review Strength Score"] = rev_theta
                    i[i.keys()[0]]["Cumulative Score"] = avg_cumul_score

                    i[i.keys()[0]]["flag"] = 1

                    for key, value in pref_scores.iteritems():
                        i[i.keys()[0]][key + " Pos"] = pref_scores[key][0]*100
                        i[i.keys()[0]][key + " Neg"] = pref_scores[key][1]*100


            #print avg_cumul_score
            #print pref_scores


        else:
            continue
    with open(out_dir + "out_DB.json", 'w') as f:
        json.dump(out_list,f,indent = 4)

main_fun(noun_scores)
