import pickle
import pandas as pd
import numpy as np
import sklearn
import fasttext
import matplotlib.pyplot as plt
import re
import string

def PredictAbuse(text):
    ft = fasttext.load_model('./saved_models/cleaned_data.bin')
    model = pickle.load(open('./saved_models/cleaned_data_pickled.sav', 'rb'))

    colors = ['green', 'red']
    labels = ['Not abusive', 'Abusive']
    xAxis = ['Not abusive', 'Abusive']

    test = ft.get_sentence_vector(text)
    test = test.reshape(1, -1)

    abuse = 'Abusive' if model.predict(test)[0] == 1 else 'Not abusive'
    proba = model.predict_proba(test)
    probabilities = 'Not abusive probability estimate: ' + str(proba[0][0]) + '\nAbusive probability estimate: ' + str(proba[0][1])

    yAxis = proba[0]
    plt.bar(xAxis, yAxis, color=colors)
    plt.title('Probability estimates', fontsize=14)
    plt.xlabel('Language', fontsize=14)
    plt.ylabel('Probability', fontsize=14)
    regex = r'[' + string.punctuation + ']'
    text = re.sub(regex, '', text)
    text = re.sub(r' ', '', text)
    plt.savefig('./img/' + text + '.png')

    print('Prediction: ' + abuse)
    print(probabilities)
    return 'Prediction: ' + abuse + '\n' + probabilities

PredictAbuse('I\'m sorry, but that is not correct, because according to the encyclopedia of Oxford, you are wrong.')