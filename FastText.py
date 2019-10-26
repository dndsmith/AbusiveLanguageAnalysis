import csv
import pandas as pd
import numpy as np
import fasttext
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import train_test_split
import sklearn
import sys
import os

# get data file to read in
print("Please enter the name of the dataset you wish to train on:")
print("\tNOTE: you should enter the name of a csv file in the data folder")
datasetName = input()
sourceCsvName = './data/' + datasetName

df = pd.read_csv(sourceCsvName, encoding='latin-1')

# remove .csv from dataset name
try:
    datasetName = datasetName[:datasetName.index('.csv')]
except:
    print("Your dataset needs to be in the .csv format. Please format it that way.")
    sys.exit()

# ask to load a previously trained fasttext model
choice = -1
model = None

if os.path.isfile('./saved_models/' + datasetName + '.bin'):
    while True:
        print(('Would you like to try to load a previous fasttext model trained on ' + datasetName + '?'))
        print('0. No\n1. Yes')
        choice = int(eval(input()))
        if choice == 0 or choice == 1:
            break

# try to load a previously trained fasttext model if user chose to do that
if choice == 1:
    try:
        model = fasttext.load_model('./saved_models/' + datasetName + '.bin')
    except:
        print('No such previously trained fasttext model exists.')
        sys.exit()

# Make sure a column for text exists
try:
    columnsNotText = list(df.columns.values)
    for i in range(len(columnsNotText)):
        if columnsNotText[i] == 'text':
            del columnsNotText[i]
            break
    
    if model == None:
        df_train = df.drop(columnsNotText, axis=1)
except:
    print("Your dataset does not have a \'text\' column. Please have a text column.")
    sys.exit()

# drop quotes, newlines, and dashes in the keywords
df.loc[:,'text'] = df.loc[:,'text'].str.replace('"', '')
df.loc[:,'text'] = df.loc[:,'text'].str.replace('\n', '')
if model == None:
    df_train.loc[:,'text'] = df_train.loc[:,'text'].str.replace('"', '')
    df_train.loc[:,'text'] = df_train.loc[:,'text'].str.replace('\n', '')

# get rid of numbers
listOfWords = df.loc[:,'text'].to_list()
i = 0
for i in range(len(listOfWords)):
    i_str = str(listOfWords[i])
    i_str = ''.join([j for j in i_str if not j.isdigit()])
    listOfWords[i] = i_str
df.loc[:,'text'] = listOfWords

if model == None:
    # create a training file for the Fasttext Unsupervised model
    print("About to train Fasttext...")
    df_train.to_csv('./data/training-TEMP.csv', encoding='latin-1', index=None, header=None)

    # train the Fasttext classification model on the text
    model = fasttext.train_unsupervised(input='./data/training-TEMP.csv',
                                        model='skipgram',
                                        dim=30,
                                        ws=10,
                                        epoch=25,
                                        thread=3,
                                        wordNgrams=2)
    
    # remove training file
    os.remove('./data/training-TEMP.csv')

    # ask if user wants to save trained fasttest model
    while True:
        print('Would you like to save this trained Fasttext model?')
        print('0. No\n1. Yes')
        choice = int(eval(input()))
        if choice == 0 or choice == 1:
            break

    if choice == 1:
        model.save_model('./saved_models/' + datasetName + '.bin')


# get word embeddings for our data
df_vecs = df['text'].apply(lambda x: pd.Series(model.get_sentence_vector(x)))
df_vecs.columns = ['vec_' + str(i) for i in range(df_vecs.shape[1])]
df_model = df.join(df_vecs)

# get name of column containing response variable
print('Please enter the name of the column that contains the response variable for the classification')
responseCol = input()

# Define X and y
X = df_model.drop(list(df.columns.values), axis=1) # drop columns from dataset to get X (the word embeddings)
y = df_model.loc[:, responseCol]

# Define and fit a logistic regression model
estimator = LogisticRegression(solver='lbfgs', multi_class='multinomial')
params = dict(C=np.logspace(0,4,20))
cross_val = RepeatedStratifiedKFold(n_splits=3, n_repeats=20, random_state=42)
clf_cross_val = GridSearchCV(estimator, param_grid=params, cv=cross_val, verbose=10, n_jobs=6, return_train_score=True, scoring="f1_micro")
print((clf_cross_val.fit(X,y)))

# get the best model
best_model = clf_cross_val.best_estimator_

# train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.333, stratify=y)

# fit best model and make predictions
best_model.fit(X_train, y_train)
y_pred = best_model.predict(X_test)
y_pred_prob = best_model.predict_proba(X_test)[:,1]
print(sklearn.metrics.classification_report(y_test, y_pred))