import pickle
import pandas as pd
import numpy as np
import sklearn
import fasttext

ft = fasttext.load_model('./saved_models/cleaned_data.csv')
model = pickle.load(open('./saved_models/cleaned_data_pickled.sav', 'rb'))

test = ft.get_sentence_vector('I love sarcasm and tearing down other people. Gosh, you are an idiot!')

print('Prediction:')
print(model.predict(test))
print('Probability:')
print(model.predict_proba(test))
print('Confidence score:')
print(model.decision_function(test))