import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

n = .1


df =  pd.read_csv('discretizedData.csv')

df.drop(['Unnamed: 0'], axis = 1, inplace = True)
df.dropna(thresh=2, axis="columns")
names = list(df)
print(len(names))
possible1Itemsets = {}
for i in range(0, len(names)):
    possible1Itemsets[names[i]] = list()
    for j in range(0, 3117):
        datum = df[names[i]][j]
        if not pd.isna(datum):
            if datum not in possible1Itemsets[names[i]]:
                possible1Itemsets[names[i]].append(datum)

#print(possible1Itemsets)
trueItemsets = {}
Itemsets1 = {}
totals =  df.count()
for i in range(0, len(names)):
    Itemsets1[names[i]] = list()
    data = df[names[i]].value_counts()
    total = totals[names[i]]
    for val in possible1Itemsets[names[i]]:
        number = data[val]
        if number/total >= n:
            Itemsets1[names[i]].append(val)
#print(Itemsets1)
trueItemsets['set1'] = Itemsets1

possible2Itemsets = {}
for i in range(0,len(names)-1):
    possible2Itemsets[names[i]] = list()
    for val in Itemsets1[names[i]]:
        for j in range(i+1,len(names)):
            for val2 in Itemsets1[names[j]]:
                #print(len(names)-1)
                itemset = ['']*(len(names))
                itemset[i] = val
                itemset[j] = val2
                possible2Itemsets[names[i]].append(itemset)

#print(possible2Itemsets)

Itemsets2 = {}
for i in range(0, len(names)-1):
    Itemsets2[names[i]] = list()
    for itemset in possible2Itemsets[names[i]]:
        indices = []
        values = []
        for q in range(0, len(names)):
            if itemset[q] != '':
                indices.append(q)
                values.append(itemset[q])
        total = 0
        if totals[names[indices[0]]] > totals[names[indices[1]]]:
            total = totals[names[indices[0]]]
        else: 
            total = totals[names[indices[1]]]
        count = 0
        for j in range(0,3117):
            if df[names[indices[0]]][j] == values[0] and df[names[indices[1]]][j] == values[1]: 
                count += 1
        if count/total > n:
            Itemsets2[names[i]].append(itemset)    

#print(Itemsets2)
trueItemsets['set2'] = Itemsets2

def possibleitemSetX(Itemsets):
    possibleXitemsets = {}
    for i in range(0,len(names)-1):
        possibleXitemsets[names[i]] = list()
        for itemset in Itemsets[names[i]]:
            indices = []
            values = []
            for q in range(0, len(names)):
                if itemset[q] != '':
                    indices.append(q)
                    values.append(itemset[q])
            for itemset2 in Itemsets[names[i]]:
                indices2 = []
                values2 = []
                for l in range(0, len(names)):
                    if itemset2[l] != '':
                        indices2.append(l)
                        values2.append(itemset2[l])
                match = True
                for z in range(0, len(indices)):
                    if indices[z] != indices2[z]:
                        match = False
                    if values[z] != values2[z]:
                        match = False
                if indices[len(indices)-1] == indices2[len(indices)-1] or values[len(indices)-1] == values2[len(indices)-1]:
                    match = False
                if match == True:
                    itemset3 = ['']*(len(names))
                    for p in range(0, len(indices)):
                        itemset3[indices[p]] = values[p]
                    itemset3[indices2[len(indices2) - 1]] = values2[len(values2) - 1]
                    possibleXitemsets[names[i]].append(itemset3)
    return possibleXitemsets

possItem3 = possibleitemSetX(Itemsets2)

def trueItemSets(possItemsets):
    trueitemsets = {}
    for i in range(0, len(names)-1):
        trueitemsets[names[i]] = list()
        print(names[i])
        for itemset in possItemsets[names[i]]:
            indices = []
            values = []
            for q in range(0, len(names)):
                if itemset[q] != '':
                    indices.append(q)
                    values.append(itemset[q])
            #print(indices, values)
            totalArray = []
            for p in range(0, len(indices)):
                totalArray.append(totals[names[indices[p]]])
            total = max(totalArray)
            count = 0
            for j in range(0,3117):
                match = True
                for z in range(0, len(indices)):
                    if df[names[indices[z]]][j] != values[z]:
                        match = False
                if match == True:
                  count += 1
            if count/total > n and itemset not in trueitemsets[names[i]]:
                trueitemsets[names[i]].append(itemset)
    return trueitemsets

set3 = trueItemSets(possItem3)
print(set3)
trueItemsets['set3'] = set3
prevKey = 'set3'
newKey = 4
allDone = False
while allDone != True:
    allDoneArray = []
    print('Calculating itemset' + str(newKey))
    for key in trueItemsets[prevKey]:
        if trueItemsets[prevKey][key] != []:
            allDoneArray.append(False)
    if allDoneArray != []:
        newposs = possibleitemSetX(trueItemsets[prevKey])
        newtrue = trueItemSets(newposs)
        #print(len(newposs['Population (millions)']), len(newtrue['Population (millions)']))
        trueItemsets['set' + str(newKey)] = newtrue
        prevKey = 'set' + str(newKey)
        newKey += 1
    else: allDone = True

finalIS = []
for key in trueItemsets:
    if key != 'set1':
        for key2 in trueItemsets[key]:
            for itemset in trueItemsets[key][key2]:
                condensedIS = {}
                for val in itemset:
                    if val != '':
                        condensedIS[names[itemset.index(val)]] = val
                finalIS.append(condensedIS)

with open('itemsets10.txt', 'w') as filehandle:  
    for listitem in finalIS:
        filehandle.write('%s\n' % listitem)

#print(trueItemsets['set3'])
