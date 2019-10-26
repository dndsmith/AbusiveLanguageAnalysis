import pickle
import pandas as pd
import numpy as np
import sklearn
import fasttext

ft = fasttext.load_model('./saved_models/cleaned_data.bin')
model = pickle.load(open('./saved_models/cleaned_data_pickled.sav', 'rb'))

test = ft.get_sentence_vector('I love sarcasm and tearing down other people. Gosh, you are an idiot!')
test = test.reshape(1, -1)

abuse = 'Abusive' if model.predict(test)[0] == 1 else 'Not abusive'
proba = model.predict_proba(test)
probabilities = 'Not abusive probability estimate: ' + str(proba[0][0]) + '\nAbusive probability estimate: ' + str(proba[0][1])

print('Prediction: ' + abuse)
print(probabilities)