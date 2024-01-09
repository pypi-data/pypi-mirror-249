from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import keras
from keras import layers
from keras.models import Model, Sequential, load_model
from keras.layers import Conv1D, Dense, Flatten, LSTM, GRU, SimpleRNN, MaxPooling1D, Dropout, Reshape
from keras.callbacks import EarlyStopping, ModelCheckpoint
from TSEnsemble import utils, arima
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np

patience = 10  # patience for early_stopping


def make_cnn(dataset,
              hidden_layers = 1,
                look_back = 12,
                filters = None,
                horizon = 1,
                kernel_size = 12,
                train_size = 0.9,
                test_size = None,
                val_size = None, 
                plot = True,
                max_plot = 70, 
                fig_size = (15, 5),
                dilation_rate = 1,
                dilation_mode = "additive",
                batch_size = 12,
                epochs = 20, 
                verbose = 0,
                n_features = 1,
                padding = 'causal',
                strides = 1,
                activation = "relu",
                dense_layers = None):
    

    """
    Generates, fits and evals CNN with set amount of layers. Callbacks used for fitting: EarlyStopping, ModelCheckpoint
    """     

    model = generate_cnn( hidden_layers = hidden_layers,
                          look_back = look_back,
                          horizon = horizon,
                          kernel_size = kernel_size,
                          dilation_mode = dilation_mode,
                          dilation_rate = dilation_rate,
                          n_features = n_features,
                          filters = filters,
                          padding = padding,
                          strides = strides,
                          activation = activation,
                          dense_layers = dense_layers)

    train_x, train_y, val_x, val_y, test_x, test_y, _, _, testScaler = utils.prepare_dataset(
        dataset, 
        train_size = train_size, 
        look_back = look_back, 
        val_size = val_size,
        test_size = test_size)
                                                                                             
    earlystop = EarlyStopping(monitor = 'val_loss', min_delta = 0, patience = 20)
    best_val = ModelCheckpoint('generated_models/cnn_model_{epoch:02d}.h5', save_best_only = True, mode = 'min') 

    model.fit(train_x,
          train_y,
          batch_size=batch_size,
          epochs=epochs,
          validation_data=(val_x, val_y),
          callbacks=[earlystop, best_val],
          verbose=verbose)
    
    utils.eval_model(model, test_x, test_y, testScaler, max_plot = max_plot, plot = plot, fig_size = fig_size)

    return model

def make_rnn(dataset, 
            hidden_layers = 1, 
            look_back = 12, 
            horizon = 1, 
            train_size = 0.9,
            test_size = None, 
            val_size = None, 
            units = 32, 
            dropout = 0.0, 
            type = 'GRU',  
            n_features = 1,
            plot = True,
            batch_size = None,
            epochs = 20,
            max_plot = 70, 
            fig_size = (15, 5)):
    """
    Generates, fits and evals a RNN with set amount of layers. Callbacks used for fitting: EarlyStopping, ModelCheckpoint
    """ 
    model = generate_rnn(hidden_layers = hidden_layers, units = units, look_back = look_back, horizon = horizon, dropout = dropout, type = type, n_features = n_features)

    if batch_size is None:
        batch_size = 16

    train_x, train_y, val_x, val_y, test_x, test_y, _, _, testScaler = utils.prepare_dataset( 
        dataset, 
        train_size = train_size, 
        look_back = look_back,  
        val_size = val_size,
        test_size = test_size)
                                                                                              
    earlystop = EarlyStopping(monitor = 'val_loss', min_delta = 0, patience = 20)
    best_val = ModelCheckpoint('generated_models/rnn_model_{epoch:02d}.h5', save_best_only = True, mode = 'min')                                                                                                        
    model.fit(train_x,
          train_y,
          batch_size = batch_size,
          epochs = epochs,
          validation_data = (val_x, val_y),
          callbacks = [earlystop, best_val],
          verbose = 0)
    
    utils.eval_model(model, test_x, test_y, testScaler, max_plot = max_plot,  fig_size = fig_size, plot = plot)

    return model

def make_transformer(dataset,
                    train_size = 0.9,
                    test_size = None,
                    val_size = None, 
                    batch_size = 32,
                    epochs = 20,
                    verbose = False,
                    look_back = 12, 
                    horizon = 1,
                    n_features = 1,
                    num_transformer_blocks = 4,
                    dropout = 0.25, 
                    head_size=256, 
                    num_heads=4, 
                    ff_dim=4,
                    mlp_units=[128],
                    mlp_dropout=0.4,
                    plot = True,
                    max_plot = 100, 
                    fig_size = (15, 5)):
    """
    Generates, fits and evals generator. Callbacks used for fitting: EarlyStopping, ModelCheckpoint
    """ 
    model = generate_transformer(look_back = look_back, 
                            horizon = horizon,
                            n_features = n_features,
                            num_transformer_blocks = num_transformer_blocks,
                            dropout = dropout, 
                            head_size=head_size, 
                            num_heads=num_heads, 
                            ff_dim=ff_dim,
                            mlp_units=mlp_units,
                            mlp_dropout=mlp_dropout)

    train_x, train_y, val_x, val_y, test_x, test_y, _, _, testScaler = utils.prepare_dataset(
        dataset, 
        train_size = train_size, 
        test_size = test_size,
        look_back = look_back, 
        val_size = val_size)

    earlystop = EarlyStopping(monitor = 'val_loss', min_delta = 0, patience = 50, restore_best_weights=True)
    best_val = ModelCheckpoint('generated_models/transformer_model_{epoch:02d}.h5', save_best_only = True, mode = 'min') 

    model.fit(train_x,
          train_y,
          batch_size = batch_size,
          epochs = epochs,
          validation_data = (val_x, val_y),
          callbacks = [earlystop, best_val],
          verbose = verbose)
    
    utils.eval_model(model, test_x, test_y, testScaler, max_plot = max_plot, plot = plot, fig_size = fig_size)

    return model

def make_seq_model(dataset, 
            layers = ["cnn", "lstm"], 
            look_back = 12,
            filters = 32,
            horizon = 1, 
            dropout = 0.0,  
            n_features = 1, 
            kernel_size = None, 
            dilation_rate = 1, 
            dilation_mode = "additive",
            optimizer = "Adam",
            loss = "mae",
            train_size = 0.9, 
            test_size = None,
            val_size = None,  
            plot = True,
            batch_size = None,
            units = 32,
            epochs = 20,
            max_plot = 70, 
            padding = 'causal',
            strides = 1,
            pool_size = 2,
            conv_activation = "relu",
            dense_layers = None,
            fig_size = (15, 5)):
    

    """
    Generates, fits and evals a sequence (cnn, rnn combination) model with set amount of layers. Callbacks used for fitting: EarlyStopping, ModelCheckpoint
    """ 
    model = generate_seq_model(layers = layers, 
                            look_back = look_back,
                            units = units,
                            filters = filters,
                            horizon = horizon, 
                            dropout = dropout, 
                            n_features = n_features,
                            kernel_size = kernel_size,
                            dilation_rate = dilation_rate, 
                            dilation_mode = dilation_mode,
                            optimizer = optimizer,
                            loss = loss,
                            padding = padding,
                            strides = strides,
                            pool_size = pool_size,
                            conv_activation = conv_activation,
                            dense_layers = dense_layers)

    if batch_size is None:
        batch_size = 16

    train_x, train_y, val_x, val_y, test_x, test_y, _, _, testScaler = utils.prepare_dataset( 
        dataset, 
        train_size = train_size, 
        look_back = look_back, 
        val_size = val_size,
        test_size = test_size)  
                                                                                       
    earlystop = EarlyStopping(monitor = 'val_loss', min_delta = 0, patience = 20)
    best_val = ModelCheckpoint('generated_models/seq_model_{epoch:02d}.h5', save_best_only = True, mode = 'min') 
    model.fit(train_x,
          train_y,
          batch_size = batch_size,
          epochs = epochs,
          validation_data = (val_x, val_y),
          callbacks = [earlystop, best_val],
          verbose = 0)
    
    utils.eval_model(model, test_x, test_y, testScaler, max_plot = max_plot, fig_size = fig_size, plot = plot)

    return model

def generate_cnn(hidden_layers = 1, 
                 look_back = 12, 
                 filters = None,
                 horizon = 1, 
                 kernel_size = 2, 
                 pool_size = 2,
                 dilation_rate = 1, 
                 dilation_mode = "multiplicative",  
                 n_features = 1, 
                 padding = 'causal',
                 strides = 1,
                 activation = "relu",
                 dense_layers = None): 
    """
    Generates a CNN with set amount of layers
    """ 
    # Create and fit the CNN
    model = Sequential()
    if filters is None:
        filters = 2 * look_back 
    # Add hidden layers
    if isinstance(filters, list):
        model.add(Conv1D(filters[0], 
                        kernel_size=kernel_size, 
                        padding=padding, 
                        strides=strides, 
                        activation=activation, 
                        dilation_rate=dilation_rate, 
                        input_shape=(look_back,  n_features)))
    else:
        model.add(Conv1D(filters, 
                kernel_size=kernel_size, 
                padding=padding, 
                strides=strides, 
                activation=activation, 
                dilation_rate=dilation_rate, 
                input_shape=(look_back,  n_features)))
        
    model.add(MaxPooling1D(pool_size = pool_size, padding='same'))
    for i in range(hidden_layers-1):
        if not (dilation_mode is None):
            if dilation_mode == "multiplicative":
                dilation_rate = dilation_rate * 2
            if dilation_mode == "additive":
                dilation_rate = dilation_rate + 1
        if isinstance(filters, list):
            model.add(Conv1D(filters[i+1], 
                            kernel_size = kernel_size, 
                            padding=padding, 
                            strides=strides, 
                            activation=activation, 
                            dilation_rate=dilation_rate))
        else:
            model.add(Conv1D(filters, 
                kernel_size = kernel_size, 
                padding=padding, 
                strides=strides, 
                activation=activation, 
                dilation_rate=dilation_rate))
        model.add(MaxPooling1D(pool_size = pool_size, padding='same'))

    # Add output layer
    model.add(Flatten())

    # Add dense layers
    if dense_layers is None:
        dense_layers = [50, horizon]
    for layer in dense_layers:
        model.add(Dense(layer))

    # compile model
    model.compile(optimizer = "Adam", loss = "mse")
    return model

def generate_rnn(hidden_layers = 1, units = 32, look_back = 12, horizon = 1, dropout = 0.0, type = 'GRU', n_features = 1):
    """
   Generates a RNN with set amount of layers
    """

    model = Sequential()
    return_sequences = hidden_layers > 1  # Last layer cannot return sequences when stacking
    if isinstance (units, int):
        # Add hidden layers
        if type.lower() == 'lstm':
            model.add(LSTM(units, dropout=dropout, return_sequences=return_sequences, input_shape=(look_back, n_features)))
        elif type.lower() == 'gru':
            model.add(GRU(units, dropout=dropout, return_sequences=return_sequences, input_shape=(look_back, n_features)))
        elif type.lower() == 'simplernn':
            model.add(SimpleRNN(units, dropout=dropout, return_sequences=return_sequences, input_shape=(look_back, n_features)))   
        else:
            print("Type is not supported!")

        for i in range(hidden_layers - 1):
            return_sequences = i < hidden_layers - 2  # Last layer cannot return sequences when stacking

            # Select and add type of layer
            if type.lower() == 'lstm':
                model.add(LSTM(units, dropout=dropout, return_sequences=return_sequences))
            elif type.lower() == 'gru':
                model.add(GRU(units, dropout=dropout, return_sequences=return_sequences))
            elif type.lower() == 'simplernn':
                model.add(SimpleRNN(units, dropout=dropout, return_sequences=return_sequences))
    else:
        # Add hidden layers
        if type.lower() == 'lstm':
            model.add(LSTM(units[0], dropout=dropout, return_sequences=return_sequences, input_shape=(look_back, n_features)))
        elif type.lower() == 'gru':
            model.add(GRU(units[0], dropout=dropout, return_sequences=return_sequences, input_shape=(look_back, n_features)))
        elif type.lower() == 'simplernn':
            model.add(SimpleRNN(units[0], dropout=dropout, return_sequences=return_sequences, input_shape=(look_back, n_features)))   
        else:
            print("Type is not supported!")

        for i in range(hidden_layers - 1):
            return_sequences = i < hidden_layers - 2  # Last layer cannot return sequences when stacking

            # Select and add type of layer
            if type.lower() == 'lstm':
                model.add(LSTM(units[i+1], dropout=dropout, return_sequences=return_sequences))
            elif type.lower() == 'gru':
                model.add(GRU(units[i+1], dropout=dropout, return_sequences=return_sequences))
            elif type.lower() == 'simplernn':
                model.add(SimpleRNN(units[i+1], dropout=dropout, return_sequences=return_sequences))
    



    model.add(Dense(horizon))

    # compile model
    if type.lower() == 'lstm':
        model.compile(optimizer='Adam', loss='mae')
    else:
        model.compile(optimizer='RMSprop', loss='mse')

    return model

def generate_transformer(look_back = 12, 
                            horizon = 1,
                            n_features = 1,
                            num_transformer_blocks = 4,
                            dropout = 0.25, 
                            head_size = 256, 
                            num_heads = 4, 
                            ff_dim = 4,
                            mlp_units = [128],
                            mlp_dropout = 0.4):
    """
   Generates a RNN with set amount of layers
    """
    model = Transformer(look_back = look_back, 
                        horizon = horizon,
                        n_features = n_features,
                        num_transformer_blocks = num_transformer_blocks,
                        dropout = dropout, 
                        head_size = head_size, 
                        num_heads = num_heads, 
                        ff_dim = ff_dim,
                        mlp_units = mlp_units,
                        mlp_dropout = mlp_dropout)
    model = model.build()
    model.compile(optimizer="Adam", 
                  loss = "mse",
                  metrics=[keras.metrics.RootMeanSquaredError(), keras.metrics.MeanAbsoluteError(), keras.metrics.MeanAbsolutePercentageError()])
    return model
    
def generate_seq_model(layers = ["cnn", "lstm"], 
                       look_back = 12, 
                       filters = 32,
                       units = 32,
                       horizon = 1, 
                       dropout = 0.0, 
                       n_features = 1, 
                       kernel_size = None, 
                       dilation_rate = 1, 
                       dilation_mode = "additive",
                       optimizer = "Adam",
                       loss = "mae",
                       padding = 'causal',
                       strides = 1,
                       pool_size = 2,
                       conv_activation = "relu",
                       dense_layers = None):
    """
   Generates a sequence (cnn, rnn combination) model
    """

    model = Sequential()
    if kernel_size is None:
        kernel_size = 2 

    unit_c = 0
    filter_c = 0
    return_sequences = len(layers) > 1
    # Add hidden layers
    if isinstance(units, int):
        if layers[0].lower() == 'lstm':
            model.add(LSTM(units, dropout=dropout, return_sequences=return_sequences, input_shape=(look_back, n_features)))
        elif layers[0].lower() == 'gru':
            model.add(GRU(units, dropout=dropout, return_sequences=return_sequences, input_shape=(look_back, n_features)))
        elif layers[0].lower() == 'simplernn':
            model.add(SimpleRNN(units, dropout=dropout, return_sequences=return_sequences, input_shape=(look_back, n_features)))   
    else:
        if layers[0].lower() == 'lstm':
            model.add(LSTM(units[0], dropout=dropout, return_sequences=return_sequences, input_shape=(look_back, n_features)))
            unit_c = unit_c + 1
        elif layers[0].lower() == 'gru':
            model.add(GRU(units[0], dropout=dropout, return_sequences=return_sequences, input_shape=(look_back, n_features)))
            unit_c = unit_c + 1
        elif layers[0].lower() == 'simplernn':
            model.add(SimpleRNN(units[0], dropout=dropout, return_sequences=return_sequences, input_shape=(look_back, n_features)))  
            unit_c = unit_c + 1

    if layers[0].lower() == 'cnn':
        if isinstance(filters, list):
            model.add(Conv1D(filters[filter_c], 
            kernel_size = kernel_size, 
            padding = padding,
            strides = strides, 
            activation = conv_activation, 
            dilation_rate = dilation_rate, 
            input_shape = (look_back,  n_features)))
            filter_c = filter_c + 1
        else:
            model.add(Conv1D(filters, 
            kernel_size = kernel_size, 
            padding = padding,
            strides = strides, 
            activation = conv_activation, 
            dilation_rate = dilation_rate, 
            input_shape = (look_back,  n_features)))
        model.add(MaxPooling1D(pool_size = pool_size, padding='same'))

    i = 0
    for layer in layers:
        if i == 0:
            i = i + 1
            continue
        return_sequences = i < len(layers) - 1
        # Select and add type of layer
        if isinstance(units, int):
            if layer.lower() == 'lstm':
                model.add(LSTM(units, dropout=dropout, return_sequences=return_sequences))
            elif layer.lower() == 'gru':
                model.add(GRU(units, dropout=dropout, return_sequences=return_sequences))
            elif layer.lower() == 'simplernn':
                model.add(SimpleRNN(units, dropout=dropout, return_sequences=return_sequences))
            elif layer.lower() == 'cnn':
                if dilation_mode == "multiplicative":
                    dilation_rate = dilation_rate * 2
                if dilation_mode == "additive":
                    dilation_rate = dilation_rate + 1
                if isinstance(filters, int):
                    model.add(Conv1D(filters, 
                        kernel_size = kernel_size, 
                        padding = padding, 
                        strides = strides, 
                        activation = conv_activation, 
                        dilation_rate = dilation_rate))
                else:
                    model.add(Conv1D(filters[filter_c], 
                                    kernel_size = filters, 
                                    padding = padding, 
                                    strides = strides, 
                                    activation = conv_activation, 
                                    dilation_rate = dilation_rate))
                    filter_c = filter_c + 1
                model.add(MaxPooling1D(pool_size = pool_size, padding='same'))
            else:
                print("Type is not supported!")
        else:
            if layer.lower() == 'lstm':
                model.add(LSTM(units[unit_c], dropout=dropout, return_sequences=return_sequences))
                unit_c = unit_c + 1
            elif layer.lower() == 'gru':
                model.add(GRU(units[unit_c], dropout=dropout, return_sequences=return_sequences))
                unit_c = unit_c + 1
            elif layer.lower() == 'simplernn':
                model.add(SimpleRNN(units[unit_c], dropout=dropout, return_sequences=return_sequences))
                unit_c = unit_c + 1
            elif layer.lower() == 'cnn':
                if dilation_mode == "multiplicative":
                    dilation_rate = dilation_rate * 2
                if dilation_mode == "additive":
                    dilation_rate = dilation_rate + 1
                if isinstance(filters, int):
                    model.add(Conv1D(filters, 
                        kernel_size = kernel_size, 
                        padding = padding, 
                        strides = strides, 
                        activation = conv_activation, 
                        dilation_rate = dilation_rate))
                else:
                    model.add(Conv1D(filters[filter_c], 
                                    kernel_size = filters, 
                                    padding = padding, 
                                    strides = strides, 
                                    activation = conv_activation, 
                                    dilation_rate = dilation_rate))
                    filter_c = filter_c + 1
                model.add(MaxPooling1D(pool_size = pool_size, padding='same'))
            else:
                print("Type is not supported!")
        i = i + 1

    if dense_layers is None:
        dense_layers = [horizon]
    for layer in dense_layers:
        model.add(Dense(int(layer)))
        
    # Add output layer
    model.compile(optimizer = optimizer, loss = loss)

    return model

class ACL:
    def __init__(self,
            order = None,
            seasonal_order = None,
            season = None,
            look_back = 12, 
            horizon = 1):

            self.order = order
            self.seasonal_order = seasonal_order
            self.season = season
            self.look_back = look_back
            self.horizon = horizon
        

    def fit(self,
                dataset,
                order = None,
                seasonal_order = None,
                season = None,
                auto = False, 
                look_back = 12, 
                horizon = 1, 
                dropout = 0.0, 
                n_features = 1, 
                kernel_size = None, 
                dilation_rate = 1, 
                dilation_mode = "additive",
                optimizer = "Adam",
                loss = "mae",
                train_size = 0.95, 
                test_size = None,
                val_size = None,  
                plot = True,
                batch_size = None,
                epochs = 20,
                max_plot = 150, 
                fig_size = (15, 5),
                verbose = True,
                padding = 'causal',
                strides = 1,
                cnn_layers = 1,
                lstm_layers = 1,
                pool_size = 2,
                fitted = True,
                dense_layers = None,
                filters = None,
                units = None,
                cnn_activation = "relu"):
        
        if self.order is None:
            if order is None:
                auto = True
            else:
                self.order = order

        if not(seasonal_order is None):
            self.seasonal_order = seasonal_order
        if not(season is None):
            self.season = season
        if not(look_back is None):
            self.look_back = look_back
        if not(horizon is None):
            self.horizon = horizon

        self.train_size = train_size
        self.test_size = test_size

        if season is None:
            if not(seasonal_order is None):
                self.season == self.seasonal_order[3]
            else: 
                self.season = self.look_back
        else:
            self.season = season

        if batch_size is None:
            batch_size = 16

        if kernel_size is None:
            kernel_size = 2 

        if auto:
            arima_model = arima.auto_arima(dataset, season = self.season)
        elif self.order is None:
            raise Exception("Order is not set and auto is False. Set auto to true?")
        else:
            arima_model = arima.make_arima(dataset, 
                            self.order, 
                            seasonal_order = self.seasonal_order,
                            train_size = train_size, 
                            test_size = test_size,
                            fig_size = fig_size,
                            max_plot = max_plot,
                            plot = False,
                            verbose = False)
            
        self.arima_model = arima_model

        train_x, train_y, val_x, val_y, test_x, test_y, trainScaler, valScaler, testScaler = utils.prepare_dataset( 
            dataset, 
            train_size = train_size, 
            look_back = self.look_back, 
            val_size = val_size)
        
        train_end = len(train_y) + self.look_back - 1
        arima_predictions = arima_model.predict(self.look_back, train_end)
        arima_val_predictions = arima_model.predict(train_end + self.look_back, train_end + len(val_y) + self.look_back - 1)
        unscaled_train_y = trainScaler.inverse_transform(train_y.reshape(-1,1)).flatten()
        unscaled_val_y = valScaler.inverse_transform(val_y.reshape(-1,1)).flatten()
        residuals = np.subtract(arima_predictions, unscaled_train_y)
        val_residuals = np.subtract(arima_val_predictions, unscaled_val_y)

        model = Sequential()
        if filters is None:
            filters = 2 * self.look_back 
        # Add hidden layers
        filters_c = 0
        units_c = 0
        if isinstance(filters, int):
            model.add(Conv1D(filters, 
                            kernel_size=kernel_size, 
                            padding=padding, 
                            strides=strides, 
                            activation=cnn_activation, 
                            dilation_rate=dilation_rate, 
                            input_shape=(look_back,  n_features)))
            model.add(MaxPooling1D(pool_size = pool_size, padding='same'))
        else:
            model.add(Conv1D(filters[filters_c], 
                            kernel_size=kernel_size, 
                            padding=padding, 
                            strides=strides, 
                            activation=cnn_activation, 
                            dilation_rate=dilation_rate, 
                            input_shape=(look_back,  n_features)))
            filters_c = filters_c + 1
            model.add(MaxPooling1D(pool_size = pool_size, padding='same'))
        for _ in range(cnn_layers-1):
            if not (dilation_mode is None):
                if dilation_mode == "multiplicative":
                    dilation_rate = dilation_rate * 2
                if dilation_mode == "additive":
                    dilation_rate = dilation_rate + 1
            if isinstance(filters, int):
                model.add(Conv1D(filters, 
                                kernel_size = kernel_size, 
                                padding=padding, 
                                strides=strides, 
                                activation=cnn_activation, 
                                dilation_rate=dilation_rate))
                model.add(MaxPooling1D(pool_size = pool_size, padding='same'))
            else:
                model.add(Conv1D(filters[filters_c], 
                kernel_size=kernel_size, 
                padding=padding, 
                strides=strides, 
                activation=cnn_activation, 
                dilation_rate=dilation_rate, 
                input_shape=(look_back,  n_features)))
                filters_c = filters_c + 1
                model.add(MaxPooling1D(pool_size = pool_size, padding='same'))

        # Add output layer
        model.add(Flatten())
        model.add(Dropout(dropout))
        model.add(Reshape((-1,1)))

        if units is None:
            units = look_back * 5

        return_sequences = lstm_layers > 1
        if isinstance(units, int):
            model.add(LSTM(units, return_sequences=return_sequences, input_shape=(self.look_back, n_features)))
        else:
            model.add(LSTM(units[units_c], return_sequences=return_sequences, input_shape=(self.look_back, n_features)))
            units_c = units_c + 1

        for i in range(lstm_layers - 1):
            return_sequences = i < lstm_layers - 2  # Last layer should not return sequences when stacking
            if isinstance(units, int):
                model.add(LSTM(units, return_sequences=return_sequences))
            else:
                model.add(LSTM(units[units_c], return_sequences=return_sequences))
                units_c = units_c + 1

        # Add dense layers
        if dense_layers is None:
            dense_layers = [look_back * 3, horizon]
        for layer in dense_layers:
            model.add(Dense(layer))

        # compile model
        model.compile(optimizer = optimizer, loss = loss)

        earlystop = EarlyStopping(monitor = 'val_loss', min_delta = 0, patience = 20)
        best_val = ModelCheckpoint('generated_models/acl_model_{epoch:02d}.h5', save_best_only = True, mode = 'min')                                                                                                        
        model.fit(train_x,
            residuals, 
            batch_size = batch_size,
            epochs = epochs, 
            validation_data = (val_x, val_residuals), 
            callbacks = [earlystop, best_val], 
            verbose=0)
        self.model = model

        if fitted == False:
          return model 

        test_y = testScaler.inverse_transform(test_y.reshape(-1,1)).flatten()
        arima_test_predictions = self.arima_model.forecast(len(test_y + self.look_back)).flatten()
        model_test_predictions = self.model.predict(test_x).flatten()
        test_predictions = np.sum([model_test_predictions, arima_test_predictions], axis = 0) 

        if plot:
            plt.figure(figsize=fig_size)
            if max_plot<len(test_y):
                plt.plot(test_y[-max_plot:], label = "Actual")
                plt.plot(test_predictions[-max_plot:], label = "Prediction")
            else:
                plt.plot(test_y, label = "Actual")
                plt.plot(test_predictions, label = "Prediction")               
            plt.ylabel('Values', fontsize=15)
            plt.legend()
            plt.show()

        if verbose:
            predicts = pd.DataFrame({'prediction' : test_predictions, 'actual' : test_y})
            print(predicts)

            rmse = utils.get_rmse(test_predictions, test_y)
            mse =  utils.get_mse(test_predictions, test_y)
            mae =  utils.get_mae(test_predictions, test_y)
            mape =  utils.get_mape(test_predictions, test_y)
            print("RMSE = {}, MSE = {}, MAE = {}, MAPE = {}".format(rmse, mse, mae, mape))
        return self
    
    def predict(self, X):
        pass
        
    def forecast(self, dataset, n, plot = True, datePlot = "date", dateStep = 1, fig_size = (10,10)):

        if isinstance(dataset, str):
         dataset = utils.ts_from_csv(dataset)

        # Create date indices for predictions
        if isinstance(dataset, pd.DataFrame) and dataset.index.inferred_type == 'datetime64':
            if dataset.index.inferred_type == 'datetime64':
                last_date = dataset.index[-1]
                delta = last_date - dataset.index[-2]
                if delta.days >= 28 and delta.days <=31:
                    delta = pd.DateOffset(months=1)
                offset = pd.tseries.frequencies.to_offset(delta)
                dateIndex = pd.date_range(last_date + delta, last_date + delta*n, freq=offset)

        # Scale dataset
        dataset = np.array(dataset)

        arima_model = ARIMA(dataset, 
                            order=self.order, 
                            seasonal_order = self.seasonal_order)
        arima_model = arima_model.fit()
        arima_forecast = arima_model.forecast(n)

        Scaler = MinMaxScaler(feature_range=(-1, 1))
        dataset = Scaler.fit_transform(dataset)
        dataset = dataset.tolist() 
        s = self.look_back
        X = dataset[-s:]
        predictions = []
        # Predicts 1 future value based on last look_back values
        for i in range(n):
            fromX = s - i
            a = X[-fromX:] if fromX > 0 else []
            fromPredictions = min(i,s)
            a = a + predictions[-fromPredictions:]
            a = np.array(a).reshape(1, -1, 1)
            prediction = self.model.predict(a, verbose = 0).tolist()
            predictions = predictions + prediction
        # Unscale predictions and add to list
        # predictions = Scaler.inverse_transform(predictions).flatten().tolist()
        predictions = np.sum([arima_forecast, np.array(predictions).flatten()], axis = 0) 
        # predictions = np.sum(arima_forecast, predictions)      
        # models_predictions = np.array(models_predictions).T.tolist()


        df = pd.DataFrame({'predictions': predictions.flatten()}, index = dateIndex)

        if plot:
            # Get indices for plotting
            if datePlot == "date":
                date = [str(d)[:10] for d in df.index.values]
            elif datePlot == "time": 
                date = [str(d)[11:16] for d in df.index.values]
            
            x = date
            y = df["predictions"].values.tolist()

            # plot predictions
            plt.figure(figsize=fig_size)
            plt.plot(x,y)
            plt.xticks(rotation = 75)
            plt.xticks(np.arange(0, len(x)+1, dateStep))
            plt.show()

        return df
        pass

    def eval(self):
        pass

class Transformer(object):



    """ Transformer Recurrent Neural Network
    """

    def __init__(self,
                look_back = 12, 
                horizon = 1,
                n_features = 1,
                num_transformer_blocks = 4,
                dropout = 0.25, 
                head_size=256, 
                num_heads=4, 
                ff_dim=4,
                mlp_units=[128],
                mlp_dropout=0.4):

        self.look_back = look_back
        self.n_features = n_features
        self.horizon = horizon

        self.head_size = head_size
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.num_transformer_blocks = num_transformer_blocks
        self.mlp_units = mlp_units
        self.mlp_dropout = mlp_dropout
        self.dropout = dropout                
        self.mlp_units=mlp_units
        self.mlp_dropout=mlp_dropout


    def transformer_encoder(self,
        inputs):

        # Normalization and Attention
        x = layers.LayerNormalization(epsilon=1e-6)(inputs)
        x = layers.MultiHeadAttention(
        key_dim=self.head_size, num_heads=self.num_heads, dropout=self.dropout)(x, x)
        x = layers.Dropout(self.dropout)(x)

        res = x + inputs

        # Feed Forward Part
        x = layers.LayerNormalization(epsilon=1e-6)(res)
        x = layers.Conv1D(filters=self.ff_dim, kernel_size=1, activation="relu")(x)
        x = layers.Dropout(self.dropout)(x)
        x = layers.Conv1D(filters=inputs.shape[-1], kernel_size=1)(x)
        return x + res


    def build(self):
        """ 
        Build the model architecture
        """

        inputs = keras.Input(shape=(self.look_back, self.n_features))
        x = inputs
        for _ in range(self.num_transformer_blocks):
            x = self.transformer_encoder(x)

        x = layers.GlobalAveragePooling1D(data_format="channels_first")(x)
        for dim in self.mlp_units:
            x = layers.Dense(dim, activation="relu")(x)
            x = layers.Dropout(self.mlp_dropout)(x)

        # output layer
        outputs = layers.Dense(self.horizon)(x)

        return keras.Model(inputs, outputs)

    # def restore(self,
    #     filepath):
    #     """ Restore a previously trained model
    #     """

    #     # Load the architecture
    #     self.model = load_model(filepath)