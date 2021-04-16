#!/usr/bin/env python
# coding: utf-8

# # Sentiment Analysis

# ## Import necessary modules

# In[57]:


import numpy as np
import pandas as pd
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score, roc_curve, auc
from sklearn.metrics import precision_recall_curve, average_precision_score
import nltk
from nltk.corpus import stopwords
from nltk.classify import SklearnClassifier


# ## Import Data

# In[66]:


data = pd.DataFrame()
data = pd.read_csv('C:\\Users\\DELL\\Desktop\\sentiment.tsv', sep='\t')
data.columns = ['sentiment', 'text']

# Check unique sentiments
print(data['sentiment'].unique())

# In[67]:

'''
# Split the data per unique sentiments
data_pos = data[data['sentiment'] == 'pos']['text']
data_neg = data[data['sentiment'] == 'neg']['text']

# Function for displaying wordcloud
def wordcloud_draw(data, color):
    words = ' '.join(data)
    cleaned_word = " ".join([word for word in words.split()
                            if 'http' not in word
                                and not word.startswith('@')
                                and not word.startswith('#')
                                and word != 'RT'
                            ])
    wordcloud = WordCloud(stopwords=STOPWORDS,
                      background_color=color,
                      width=2500,
                      height=2000
                     ).generate(cleaned_word)
    plt.figure(1,figsize=(13, 13))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
    
print("Positive words")
wordcloud_draw(data_pos, 'white')
print("Negative words")
wordcloud_draw(data_neg, 'black')
'''

# ## Splitting the dataset into train and test set
data_kf = []
stopwords_set = set(stopwords.words("english"))
for index, row in data.iterrows():
    temp = []
    words_filtered = [e.lower() for e in row.text.split() if len(e) >= 3]
    words_cleaned = [word for word in words_filtered
        if 'http' not in word
        and not word.startswith('@')
        and not word.startswith('#')
        and word != 'RT']
    words_without_stopwords = [word for word in words_cleaned if not word in stopwords_set]
    temp.append(words_without_stopwords)
    temp.append(row.sentiment)
    data_kf.append(temp)

x = []
y = []
for i in range(len(data_kf)):
    x.append(data_kf[i][0])
    y.append(data_kf[i][1])

random_state = np.random.RandomState(0)
clf = RandomForestClassifier(random_state=random_state)
cv = StratifiedKFold(n_splits=10,shuffle=False)

# In[60]:
auc = []
i = 1
# Split dataset into train and test per unique sentiment

for train,test in cv.split(x,y):
    print(train)
    print(test)
    print("Iteration", i)
    # ## Removing Stopwords
    tweets_train = []

    x = pd.DataFrame(train)
    for index, row in x.iterrows():
        words_filtered = [e.lower() for e in row.text.split() if len(e) >= 3]
        words_cleaned = [word for word in words_filtered
            if 'http' not in word
            and not word.startswith('@')
            and not word.startswith('#')
            and word != 'RT']
        words_without_stopwords = [word for word in words_cleaned if not word in stopwords_set]
        tweets_train.append((words_without_stopwords, row.sentiment))

    tweets_test = []
    stopwords_set = set(stopwords.words("english"))
    for index, row in test.iterrows():
        words_filtered = [e.lower() for e in row.text.split() if len(e) >= 3]
        words_cleaned = [word for word in words_filtered
            if 'http' not in word
            and not word.startswith('@')
            and not word.startswith('#')
            and word != 'RT']
        words_without_stopwords = [word for word in words_cleaned if not word in stopwords_set]
        tweets_test.append((words_without_stopwords, row.sentiment))

    # ## Extracting word features

    '''
    def get_words_in_tweets(tweets):
        all = []
        for (words, sentiment) in tweets:
            all.extend(words)
        return all

    def get_word_features(wordlist):
        wordlist = nltk.FreqDist(wordlist)
        features = wordlist.keys()
        return features

    w_features = get_word_features(get_words_in_tweets(tweets))
    '''
    def extract_features(document):
        document_words = set(document)
        features = {}
        for word in w_features:
            features['contains(%s)' % word] = (word in document_words)
        return features

    # Training the Naive Bayes classifier
    training_set = nltk.classify.apply_features(extract_features,tweets_train)
    testing_set = nltk.classify.apply_features(extract_features,tweets_test)
    classifier = nltk.NaiveBayesClassifier.train(training_set)

    # Testing the Naive Bayes classifier
    test_result = []
    gold_result = []

    for i in range(len(testing_set)):
        test_result.append(classifier.classify(testing_set[i][0]))
        gold_result.append(testing_set[i][1])

    CM = nltk.ConfusionMatrix(gold_result, test_result)
    print(CM)
    print("Naive Bayes Algo accuracy percent:"+str((nltk.classify.accuracy(classifier, testing_set))*100)+"\n")
    print('\nClasification report:\n', classification_report(gold_result, test_result))

    TN = CM._confusion[0][0]
    FN = CM._confusion[0][1]
    TP = CM._confusion[1][0]
    FP = CM._confusion[1][1]
    TPR = TP / (TP + FN)
    FPR = FP / (FP + TN)

    auc.append(metrics.auc(fpr, tpr))
    print("AUC : ", str(metrics.auc(fpr, tpr)))

    i = i + 1
