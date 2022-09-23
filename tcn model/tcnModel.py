import pandas as pd
from tcn import TCN, tcn_full_summary
from tensorflow.keras import Sequential
from tensorflow.keras import callbacks
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import RepeatVector
from tensorflow.keras.layers import Dropout
from tensorflow.keras import regularizers
from tensorflow.keras import optimizers
from tensorflow.keras import initializers
from tcn import compiled_tcn
import numpy as np
from sklearn import preprocessing

#%%


class mainModel():

    def __init__(self, batch_size, time_steps, input_dim, output_timesteps, output_dim, epochs, kernel_size, nb_filters, dropout, patience, testLen, nb_stacks):
        self.batch_size, self.time_steps, self.input_dim, self.output_timesteps, self.output_dim, self.epochs, self.kernel_size, self.nb_filters, self.dropout, self.patience, self.testLen, self.nb_stacks= batch_size, time_steps, input_dim, output_timesteps, output_dim, epochs, kernel_size, nb_filters, dropout, patience, testLen, nb_stacks

    # Gauss rank scaler
    def getMStratData(self, data, subsampleSize):
        from gauss_rank_scaler import GaussRankScaler
        # Del first row
        data = data.drop(data.index[0])
        data = data.drop(columns=["sd_price","sd_quoteQty"])
        # Take sub sample
        if subsampleSize == None:
            sampled_data = data
        else:
            sampled_data = data[:subsampleSize]
        # Take y 
        y = sampled_data.price.to_numpy()
        #sampled_data = sampled_data.drop(columns=["delta_percent_price"])
        # GaussRankScaler only X
        scaler = GaussRankScaler()
        X = scaler.fit_transform(sampled_data)
        
        #X = sampled_data.to_numpy()

    
        X_train, y_train, X_test, y_test = [],[],[],[]
        # shape ==>(sampled data, time_steps, input_dim)
        #train
        for i in range(self.time_steps,len(X)-self.testLen-self.output_timesteps):
            X_train.append(X[i-self.time_steps:i])
            y_train.append(y[i:i+self.output_timesteps])
            
        # X_test.append(X[-self.time_steps-self.output_timesteps:-self.output_timesteps,:])    
        # y_test.append(y[-self.output_timesteps:])
        
        #test
        for i in range(-self.testLen, -self.time_steps-self.output_timesteps):
            X_test.append(X[i:i+self.time_steps])
            y_test.append(y[i+self.time_steps:i+self.time_steps+self.output_timesteps])
            
        X_train, y_train, X_test,y_test= np.array(X_train), np.array(y_train), np.array(X_test) ,np.array(y_test)
        y_train=np.reshape(y_train,(y_train.shape[0],self.output_timesteps,self.output_dim))
        X_train=np.reshape(X_train,(X_train.shape[0],self.time_steps,self.input_dim))
        y_test=np.reshape(y_test,(y_test.shape[0],self.output_timesteps,self.output_dim))
        
        #y multiply test
        y_train = y_train
        return sampled_data, X, y, X_train, y_train, X_test,y_test
        
    #sampled_data, sampled_scaled_data,y, x_train, y_train, x_test, y_test = getGaussRankData(data,subsampleSize)
    
    def getSeq2SeqData(self, data, subsampleSize):
        from gauss_rank_scaler import GaussRankScaler
        import math
        # Del first row
        data = data.drop(data.index[0])
        data = data.drop(columns=["delta_percent_price"])
        # Take y
        y = data.price
        # Remove useless y
        new_y = y[self.time_steps:]
        # Updated y in Dataframe 
        data = data.drop(columns=['price'])
    
        # Take sub sample
        if subsampleSize == None:
            subsampleSize = (math.floor(len(data)/self.time_steps)*self.time_steps)-self.time_steps
        else:
            subsampleSize = math.floor(subsampleSize/self.time_steps)*self.time_steps
        print("Updated subsampleSize : ", subsampleSize)
        
        sampled_data = data[:subsampleSize]
        sampled_data["price"] = y[:subsampleSize]
        new_y = new_y[:subsampleSize]
        # scaling and convert to np
        scaler = GaussRankScaler()
        #X_data = scaler.fit_transform(sampled_data)
        X_data = sampled_data.to_numpy()
        X_data = np.array(np.vsplit(X_data,len(X_data)/self.time_steps))
        y_data = np.array(np.split(new_y,len(new_y)/self.time_steps))
        y_data = np.reshape(y_data,(y_data.shape[0],self.output_timesteps,self.output_dim))
        print(np.shape(X_data))
        print(np.shape(y_data))
        # Split train test 
        X_train = X_data[:-1,:,:]
        X_test = X_data[-1:,:,:]
        y_train = y_data[:-1,:,]
        y_test = y_data[-1:,:,]
        X_test=np.reshape(X_test,(1,self.time_steps,self.input_dim))
        y_test=np.reshape(y_test,(1,self.output_timesteps,self.output_dim))
        
        #y multiply test
        y_train = y_train
        return sampled_data,X_data,y_data,X_train, y_train, X_test,y_test
        
    
    # The receptive field tells you how far the model can see in terms of timesteps.
    # print('Receptive field size =', tcn_layer.receptive_field)
    
    
    def modelCompute(self, x_train, y_train, x_test):
        
        ini = initializers.GlorotUniform()
        
        TCNLayer = TCN(input_shape=(self.time_steps, self.input_dim),return_sequences=True, kernel_size=self.kernel_size, nb_filters=self.nb_filters, dropout_rate=self.dropout, nb_stacks=self.nb_stacks, use_batch_norm=True, kernel_initializer=ini  ,dilations=(1, 2, 4, 8, 16, 32, 64))
        print('Receptive field size =', TCNLayer.receptive_field)
        
        model = Sequential([
            TCNLayer, 
            

            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            Dense(self.nb_filters, activation='relu'),
            
            Dense(self.output_dim ) # output layer
        ])
        
        model.summary()
    
        
        model.compile(optimizer='Adam', loss='mae')
        print("loss = mae")

        
        
        
        
        #callback
        es_callback = callbacks.EarlyStopping(monitor='loss', patience=self.patience)
        
        model.fit(x_train, y_train, epochs=self.epochs, batch_size = self.batch_size)#, callbacks=[es_callback], validation_split=0.2)
        
        #save model
        model.save('./model/tcn')
        
        y_pre = model.predict(x_test)


        #further mod
        y_pre = y_pre


        return y_pre
        


