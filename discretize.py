import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import math

df =  pd.read_csv('election_dataframe.csv')
#df.drop(['Country', 'Country Code', 'Happiness Rank'], axis = 1, inplace = True)
names = list(df)

print(names)

#Make GDP a number
# for i in range(0, 202):
#     s = df["GDP per Capita"][i]
#     if not pd.isna(s):
#         df["GDP per Capita"][i] = float(s.replace("$", "").replace(",", ""))
dtypes = df.dtypes
# print(dtypes["POV05_2016"])
# print(df["POV05_2016"])
#Discretize data
for i in range(0, len(names)):
    if dtypes[i] != object:
        df.to_csv('discretizedData.csv')
        # if names[i] != "Region_x" and names[i] != "Region_y":
        halfStdev = df[names[i]].std()/2
        dRange = df[names[i]].max() - df[names[i]].min()
        if not pd.isna(halfStdev) and not pd.isna(dRange):
            bins = math.floor(dRange/halfStdev)
            print(names[i], dRange, halfStdev, bins)
            discretized = pd.cut(df[names[i]],bins)
            for j in range(0, 3117):
                if not pd.isna(df[names[i]][j]):
                    df[names[i]][j] = (discretized[j].left + discretized[j].right)/2

df.to_csv('discretizedData.csv')
