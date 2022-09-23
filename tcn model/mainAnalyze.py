#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 16:49:49 2022

@author: alex
"""

import pandas as pd
from keras.models import load_model
from sklearn.metrics import mean_absolute_percentage_error
from math import sqrt
import matplotlib.pyplot as plt
from tcnModel import mainModel
from tcn import TCN, tcn_full_summary


# Step 9. Analyze and further visualize

jsonName = "trade-2022-3"
data = pd.read_json(f"./data/{jsonName}.json")
data.drop(data.index[0:3],0,inplace=True)

#load model
model = load_model('./model/tcn')

#get organised data

#must match param of model
batch_size = 64
time_steps = 15
input_dim = 4
output_timesteps = 15
output_dim = 1
epochs = 3000
kernel_size = 4
nb_filters = 256
dropout = 0.05
patience = 50
testLen = 100
nb_stacks = 1
subsampleSize = None

mainModel = mainModel(batch_size, time_steps, input_dim, output_timesteps, output_dim, epochs, kernel_size, nb_filters, dropout, patience, testLen, nb_stacks)

sampled_data, sampled_scaled_data, y , x_train, y_train, x_test, y_test = mainModel.getSeq2SeqData(data, subsampleSize)

#%%
#loss vs epoch

# training_loss = model.history['loss']
# epoch_count = range(1, len(training_loss) + 1)

# plt.plot(epoch_count, training_loss, 'r-')
# plt.xlabel('Epoch')
# plt.ylabel('Loss')
# plt.show();

#%%
#predict strat 
stratDf = pd.DataFrame(data={'CALL': [0],'CallSuccess': [0],'CallFail': [0],'PUT': [0],'PutSuccess': [0],'PutFail': [0],'STAY': [0], 'Gain': [0]})
startSet = 0
cutOffSet = 0

#strat param
callActThreshold = 0.001 
putActThreshold = 0.001 
stopGain = 0.001 #0.1%

steps = 0
for i in range(startSet, len(x_train)-cutOffSet):
    predict = model.predict(x_train[i:i+1,:,:])
    true = y_train[i:i+1,:,:]
    predict = predict.flatten()
    true = true.flatten()
    plt.plot(range(1,len(predict)+1), predict, label = "prediction")
    plt.plot(range(1,len(true)+1), true, label = "true")
    plt.legend()
    plt.title('prediction vs test')
    plt.show()
    
    if predict[0] > true[0]:
        if predict[4]-predict[0] > predict[0]*callActThreshold:
            stratDf.at[0,'CALL'] = stratDf.at[0,'CALL']+1
            if true[4]-true[0] > true[0]*stopGain:
                stratDf.at[0,'CallSuccess'] = stratDf.at[0,'CallSuccess']+1
            else:
                stratDf.at[0,'CallFail'] = stratDf.at[0,'CallFail']+1
        else:
            stratDf.at[0,'STAY'] = stratDf.at[0,'STAY']+1
    elif predict[0] < true[0]:
        if predict[4]-predict[0] < predict[0]*putActThreshold*-1:
            stratDf.at[0,'PUT'] = stratDf.at[0,'PUT']+1
            if true[4]-true[0] < true[0]*stopGain*-1:
                stratDf.at[0,'PutSuccess'] = stratDf.at[0,'PutSuccess']+1
            else:
                stratDf.at[0,'PutFail'] = stratDf.at[0,'PutFail']+1
        else:
            stratDf.at[0,'STAY'] = stratDf.at[0,'STAY']+1
    else:
        stratDf.at[0,'STAY'] = stratDf.at[0,'STAY']+1
    stratDf.at[0,'Gain'] = stratDf.at[0,'CallSuccess']+stratDf.at[0,'PutSuccess']-stratDf.at[0,'CallFail']-stratDf.at[0,'PutFail']
    steps = steps + 1
    print("Number: "+str(steps))
    print(stratDf)