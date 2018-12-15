#!/usr/bin/python
# -*- coding: utf-8 -*-

# Code source: Gaël Varoquaux
# Modified for documentation by Jaques Grobler
# License: BSD 3 clause

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn import datasets
from sklearn.model_selection import train_test_split

#Data Cleaning
df =  pd.read_csv('election_dataframe.csv')
df.set_index(['State', 'FIPS Code'], inplace=True)
df.sort_index(inplace=True)
df = df.select_dtypes(include='number')
colavgs = {}
for col in df:
    colavgs[col] = df[col].mean()
df.fillna(value = colavgs, inplace=True)
df.drop([('SD', 46102), ('MT', 30113), ('VA', 51515), ('VA', 51560)], inplace=True)
Y = df['Democrats 2016'] - df['Republicans 2016']
Y[(Y >= 0.0)] = 1
Y[(Y < 0.0)] = 0
df.drop(columns = ['Democrats 2016', 'Republicans 2016', 'POV05_2016', 'CI90LB05_2016', 'CI90UB05_2016', 'PCTPOV05_2016', 'CI90LB05P_2016', 'CI90UB05P_2016'], inplace=True)
df.dropna(axis = 'rows', inplace=True)
X = df
#Split Training/Testing Data
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.25)

#Logistic Regression
logreg = LogisticRegression(C=1e5, solver='lbfgs', multi_class='multinomial')
logreg.fit(x_train, y_train)
#print(logreg.predict(x_test), y_test)
print("Logistic Regression running on a 25/75 test train split.")
print("Logistic Regression parameters:", logreg.coef_[0])
for i in range(0, len(x_train.columns)):
    print(x_train.columns[i], logreg.coef_[0][i])
print("Logistic Regression accuracy is ",round(logreg.score(x_test, y_test)*100,3),"%", sep='')

