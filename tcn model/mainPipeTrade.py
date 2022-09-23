import pandas as pd
import numpy as np


jsonName = "trade-2022-3"
data = pd.read_json(f"./data/{jsonName}.json")


# Step 4. setup model hyperparam

from tcnModel import mainModel

#params
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

# Step 5. data cleaning

sampled_data, sampled_scaled_data, y , x_train, y_train, x_test, y_test = mainModel.getSeq2SeqData(data,subsampleSize)

print(np.shape(x_train))
print(np.shape(y_train))

# Step 6. model train
prediction = mainModel.modelCompute(x_train, y_train, x_test)

# Step 7. evaluate

prediction = prediction.flatten()
y_test = y_test.flatten()

print('===test===')
print(y_test)
print(prediction)

from sklearn.metrics import mean_absolute_percentage_error
from math import sqrt
import matplotlib.pyplot as plt

mapeTest = mean_absolute_percentage_error(y_test, prediction)


print("===mapeTest===")
print(mapeTest)

# Step 8. initial visualize

plt.plot(range(1,len(prediction)+1), prediction, label = "prediction")
plt.plot(range(1,len(y_test)+1),y_test, label = "true")
plt.legend()
plt.title('test')
plt.savefig('testSetResult.png')

