def lstmModelCompute(self, x_train, y_train, x_test):
        from keras.layers import LSTM
        model=Sequential()
        model.add(LSTM(units=64,return_sequences=False,input_shape=(x_train.shape[0],1)))
        model.add(Dense(1))
        model.summary()

        model.compile(optimizer="adam", loss='mse')
        print("loss = mse")
        
        model.fit(x_train, y_train, epochs=self.epochs, batch_size = self.batch_size, validation_split=0.1 )
        
        y_pre = model.predict(x_test)
        y_train_pre = model.predict(x_train[0:10,:,:])

        y_pre = y_pre/100
        y_train_pre = y_train_pre/100

        return y_train_pre , y_pre