#!/usr/bin/env python
# coding: utf-8

# # Sentiment Analysis

# ## Import necessary modules

# In[1]:


import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
xml_path = 'C:\\Users\\DELL\\Desktop\\ABSA-15_Restaurants_Train_Final.xml'
def parse_data_2015(xml_path):
    container = []                                              
    reviews = ET.parse(xml_path).getroot()                      
    
    for review in reviews:  
        sentences = review.getchildren()[0].getchildren()       
        for sentence in sentences:                                  
            sentence_text = sentence.getchildren()[0].text          
            
            try:                                                     
                opinions = sentence.getchildren()[1].getchildren()
            
                for opinion in opinions:                                
                    polarity = opinion.attrib["polarity"]
                    target = opinion.attrib["target"]
        
                    row = {"sentence": sentence_text, "sentiment":polarity}   
                    container.append(row)                                                              
                
            except IndexError: 
                row = {"sentence": sentence_text}        
                container.append(row)                                                               
                
    return pd.DataFrame(container)
ABSA_df = parse_data_2015(xml_path)
ABSA_df.head()


# In[2]:


ABSA_df.isnull().sum()


# In[3]:


print("Original:", ABSA_df.shape)
ABSA_dd = ABSA_df.drop_duplicates()
dd = ABSA_dd.reset_index(drop=True)
print("Drop Dupicates:", dd.shape)
dd_dn = dd.dropna()
df = dd_dn.reset_index(drop=True)
print("Drop Nulls:", df.shape)


# In[4]:


df.sentence[17]


# In[5]:


from nltk.tokenize import word_tokenize
tokens = word_tokenize(df.sentence[17])
print(tokens)


# In[6]:


from nltk.corpus import stopwords
stop_words = stopwords.words('english')
print([i for i in tokens if i not in stop_words])


# In[7]:


df.sentence[24]


# In[8]:


lower_case = df.sentence[24].lower()
lower_case


# In[9]:


appos = {
"aren't" : "are not",
"can't" : "cannot",
"couldn't" : "could not",
"didn't" : "did not",
"doesn't" : "does not",
"don't" : "do not",
"hadn't" : "had not",
"hasn't" : "has not",
"haven't" : "have not",
"he'd" : "he would",
"he'll" : "he will",
"he's" : "he is",
"i'd" : "I would",
"i'd" : "I had",
"i'll" : "I will",
"i'm" : "I am",
"isn't" : "is not",
"it's" : "it is",
"it'll":"it will",
"i've" : "I have",
"let's" : "let us",
"mightn't" : "might not",
"mustn't" : "must not",
"shan't" : "shall not",
"she'd" : "she would",
"she'll" : "she will",
"she's" : "she is",
"shouldn't" : "should not",
"that's" : "that is",
"there's" : "there is",
"they'd" : "they would",
"they'll" : "they will",
"they're" : "they are",
"they've" : "they have",
"we'd" : "we would",
"we're" : "we are",
"weren't" : "were not",
"we've" : "we have",
"what'll" : "what will",
"what're" : "what are",
"what's" : "what is",
"what've" : "what have",
"where's" : "where is",
"who'd" : "who would",
"who'll" : "who will",
"who're" : "who are",
"who's" : "who is",
"who've" : "who have",
"won't" : "will not",
"wouldn't" : "would not",
"you'd" : "you would",
"you'll" : "you will",
"you're" : "you are",
"you've" : "you have",
"'re": " are",
"wasn't": "was not",
"we'll":" will",
"didn't": "did not"
}


# In[10]:


words = lower_case.split()
reformed = [appos[word] if word in appos else word for word in words]
reformed = " ".join(reformed) 
reformed


# In[11]:


tokens


# In[12]:


words = [word for word in tokens if word.isalpha()]
words


# In[13]:


df.sentence[24]


# In[18]:


from gensim.utils import lemmatize
lemm = lemmatize(df.sentence[24])
lemm


# In[19]:


df.sentence[17]


# In[23]:


lemmatize(df.sentence[17])


# In[26]:


df.sentence[24].decode("utf-8-sig")


# In[47]:


import time
from tqdm import tqdm
def cleaning_function(tips):
    all_ = []
    for tip in tqdm(tips):
        time.sleep(0.0001)
        
#       Decoding function
        decode = tip.encode("utf-8-sig").decode("utf-8-sig")
    
#       Lowercasing before negation
        lower_case = decode.lower()
    
#       Replace apostrophes with words
        words = lower_case.split()
        split = [appos[word] if word in appos else word for word in words]
        reformed = " ".join(split) 
        
#       Lemmatization
        lemm = lemmatize(lower_case)
        all_.append(lemm)
        
    return all_

def separate_word_tag(df_lem_test):
    words=[]
    types=[]
    df= pd.DataFrame()
    for row in df_lem_test:
        sent = []
        type_ =[]
        for word in row:
            split = word.split('/')
            sent.append(split[0])
            type_.append(split[1])

            words.append(' '.join(word for word in sent))
            types.append(' '.join(word for word in type_))
    df['lem_words']= words
    df['lem_tag']= types
    return df


# In[48]:


word_tag = cleaning_function(df.sentence)
lemm_df = separate_word_tag(word_tag)
# concat cleaned text with original
df_training = pd.concat([df, lemm_df], axis=1)
df_training['word_tags'] = word_tag
df_training.head()


# In[ ]:


# reset index just to be safe
df_training = df_training.reset_index(drop=True)
#check null values
df_training.isnull().sum()


# In[ ]:


# empty values
df_training[df_training['lem_words']=='']


# In[ ]:


# drop these rows
print df_training.shape
df_training = df_training.drop([475, 648, 720])
df_training = df_training.reset_index(drop=True)
print df_training.shape


# In[ ]:


# load the data
fs = pd.read_csv(‘./foursquare/foursquare_csv/londonvenues.csv’)
# use cleaning functions on the tips
word_tag_fs = cleaning_function(fs.tips)
lemm_fs = separate_word_tag(word_tag_fs)
# concat cleaned text with original
df_fs_predict = pd.concat([fs, lemm_fs], axis=1)
df_fs_predict['word_tags'] = word_tag_fs
# separate the long lat
lng=[]
lat=[]
for ll in df_fs_predict['ll']:
    lnglat = ll.split(',')
    lng.append(lnglat[0])
    lat.append(lnglat[1])
df_fs_predict['lng'] =lng
df_fs_predict['lat'] =lat
#  drop the ll column
df_fs_predict = df_fs_predict.drop(['ll'], axis=1)
df_fs_predict.head()


# In[ ]:


# save clean foursquare to csv
df_fs_predict.to_csv('./foursquare/foursquare_csv/foursquare_clean.csv', header=True, index=False, encoding='UTF8')

