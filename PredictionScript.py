import pickle
import pandas as pd
import numpy as np
import sklearn

model = pickle.load(open('./saved_models/cleaned_data_pickled.sav', 'rb'))