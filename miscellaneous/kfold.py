#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas
from sklearn.model_selection import KFold
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVR
import numpy as np


# In[2]:


dataset = pandas.read_csv('C:\\Users\\DELL\\Desktop\\housing.csv', sep=',')


# In[3]:


X = dataset.iloc[:, [0, 12]]
y = dataset.iloc[:, 13]


# In[4]:


scaler = MinMaxScaler(feature_range=(0, 1))
X = scaler.fit_transform(X)


# In[5]:


scores = []
best_svr = SVR(kernel='rbf')
cv = KFold(n_splits=10, random_state=42, shuffle=False)
for train_index, test_index in cv.split(X):
    print("Train Index: ", train_index, "\n")
    print("Test Index: ", test_index)

    X_train, X_test, y_train, y_test = X[train_index], X[test_index], y[train_index], y[test_index]
    best_svr.fit(X_train, y_train)
    scores.append(best_svr.score(X_test, y_test))


# In[ ]:


print(np.mean(scores))


# In[ ]:


cross_val_score(best_svr, X, y, cv=10)


# In[ ]:


cross_val_predict(best_svr, X, y, cv=10)

