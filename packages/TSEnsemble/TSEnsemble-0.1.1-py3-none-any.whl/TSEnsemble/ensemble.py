import lightgbm as lgb
import numpy as np
from keras.callbacks import EarlyStopping, ModelCheckpoint
from TSEnsemble import utils
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import pandas as pd
from catboost import CatBoostRegressor
from statsmodels.tsa.arima.model import ARIMA, ARIMAResultsWrapper, ARIMAResults
import math

class Ensemble():
  """ 
  Ensemble of a models class, that takes a bunch of models and uses them as features for a regressor (by default LGBM).
  """
  def __init__(self, models = [], regressor = "wmean", dataset = None, regr_params = None, params = None):
    """ 
    Initialize a model object
    """
    self.model = None
    self.models = models
    self.dataset = dataset
    self.regressor = regressor
    if not(params is None):
        self.regr_params = params
    else:
        self.regr_params = regr_params
    self.test_x = None
    self.test_y = None
  

  def fit(self,
          dataset,
          look_back = None,
          fit_models = True,
          train_size = 0.9,
          metric = "rmse",
          regr_params = None,
          test_size = None, 
          features = [],
          val_size = 0.1, 
          models_val_size = None,
          regr_val_size = None,
          train_models_size = 0.8,
          batch_size = 32,
          epochs = 20,
          early_stop = None,
          models_callbacks = [EarlyStopping(monitor='val_loss', min_delta=0, patience=10),
                      ModelCheckpoint('generated_models/cnn_model_{epoch:02d}.h5', save_best_only=True, mode='min') ]):
    """ 
    Fit a model based on object models and a full given dataset.
    """
    
    # val_num = int(len(dataset) * val_size * train_size) 
    # train_num = int(len(dataset) * train_size) - val_num 
    # test_num = int(len(dataset) * (1 - train_size)) + 1

    ensemble_val_x = list()
    ensemble_train_x =  list()
    ensemble_test_x =  list()

    if look_back is None:
      max_lb = 0
      for model in self.models:
        if not(utils.get_seasonality(model) is None) and max_lb < utils.get_seasonality(model):
          if len(self.models) == 1:
            max_lb = utils.get_seasonality(model)
      if max_lb is None: 
        look_back = 1
      else:
        look_back = max_lb

    if batch_size is None:
       batch_size = look_back

    if not(isinstance(dataset, np.ndarray)):
        dataset = dataset.values
        dataset = dataset.astype('float64')

    if (np.isnan(dataset).any()):
        dataset = utils.interpolate_nan(dataset)

    if train_size is None: 
        if test_size is None:
            train_size = 0.9
        else:
            train_size = 1 - test_size

    if models_val_size is None and regr_val_size is None:
        models_val_size = val_size
        regr_val_size = val_size
    elif models_val_size is None:
        models_val_size = val_size
    elif regr_val_size is None:
        regr_val_size = val_size

    val_size = (train_size * val_size)

    # split data: [models_train : models_val : regr_train : regr_val : test]
    # train_size = train_size - val_size
    train_c = math.floor(len(dataset) * train_size)
    models_train_c = math.floor(train_c * train_models_size)
    regr_train_c = math.floor(train_c * (1-train_models_size))
    models_val_c = math.floor(models_train_c * models_val_size)
    regr_val_c = math.floor(regr_train_c * regr_val_size)
    models_train_num = models_train_c - models_val_c
    models_val_num = models_train_num + models_val_c
    regr_train_num = models_val_num + regr_train_c - regr_val_c
    regr_val_num = regr_train_num + regr_val_c

    models_train = dataset[:models_train_num, :]
    models_val = dataset[models_train_num:models_val_num, :]
    regr_train = dataset[models_val_num:regr_train_num, :]
    regr_val =  dataset[regr_train_num:regr_val_num, :]
    test = dataset[regr_val_num:, :]

    # normalize dataset separately
    unscaled_models_train = models_train.copy() 
    unscaled_models_val = models_val.copy()     
    unscaled_regr_train = regr_train.copy()   
    unscaled_regr_val = regr_val.copy() 

    models_trainScaler = MinMaxScaler(feature_range=(-1, 1))
    models_train = models_trainScaler.fit_transform(models_train)

    regr_trainScaler = MinMaxScaler(feature_range=(-1, 1))
    regr_train = regr_trainScaler.fit_transform(regr_train)

    models_valScaler = MinMaxScaler(feature_range=(-1, 1))
    models_val = models_valScaler.fit_transform(models_val)

    regr_valScaler = MinMaxScaler(feature_range=(-1, 1))
    regr_val = regr_valScaler.fit_transform(regr_val)

    testScaler = MinMaxScaler(feature_range=(-1, 1))
    test = testScaler.fit_transform(test)   

    # reshape into X=t and Y=t+1
    scaled_dataset = np.array(models_train.tolist() + models_val.tolist() + regr_train.tolist() + regr_val.tolist() + test.tolist())
    scaled_x, scaled_y = utils.create_dataset(scaled_dataset, look_back)
    models_train_x = scaled_x[:models_train_num - look_back]
    models_train_y = scaled_y[:models_train_num - look_back]
    models_val_x = scaled_x[models_train_num - look_back:models_val_num - look_back]
    models_val_y = scaled_y[models_train_num - look_back:models_val_num - look_back]
    regr_train_x = scaled_x[models_val_num - look_back:regr_train_num - look_back]
    regr_train_y = scaled_y[models_val_num - look_back:regr_train_num - look_back]
    regr_val_x = scaled_x[regr_train_num - look_back:regr_val_num - look_back]
    regr_val_y = scaled_y[regr_train_num - look_back:regr_val_num - look_back]
    test_x = scaled_x[regr_val_num - look_back:]
    test_y = scaled_y[regr_val_num - look_back:]

    # reshape input to be [samples, time steps, features]
    models_train_x = np.reshape(models_train_x, (models_train_x.shape[0], models_train_x.shape[1], 1))
    regr_train_x = np.reshape(regr_train_x, (regr_train_x.shape[0], regr_train_x.shape[1], 1))
    models_val_x = np.reshape(models_val_x, (models_val_x.shape[0], models_val_x.shape[1], 1))
    regr_val_x = np.reshape(regr_val_x, (regr_val_x.shape[0], regr_val_x.shape[1], 1))
    test_x = np.reshape(test_x, (test_x.shape[0], test_x.shape[1], 1))
                                                                             
    arima_data = list(unscaled_models_train) + list(unscaled_models_val)
    scaled_models_val_y = np.copy(models_val_y)
    scaled_models_train_y = np.copy(models_train_y)
    scaled_regr_train_y = np.copy(regr_train_y)
    scaled_regr_val_y = np.copy(regr_val_y)
    test_y = testScaler.inverse_transform(test_y.reshape(-1, 1)).flatten()
    models_train_y = models_trainScaler.inverse_transform(models_train_y.reshape(-1, 1)).flatten()
    regr_train_y = regr_trainScaler.inverse_transform(regr_train_y.reshape(-1, 1)).flatten()
    regr_val_y = regr_valScaler.inverse_transform(regr_val_y.reshape(-1, 1)).flatten()
    models_val_y = models_valScaler.inverse_transform(models_val_y.reshape(-1, 1)).flatten()
    metrics = []

    def model_fit(model, arima_data = None, models_train_x = None, scaled_models_train_y = None, models_val_x = None, scaled_models_val_y = None, features = None):
            if isinstance(model, ARIMA) or isinstance(model, ARIMAResultsWrapper)  or isinstance(model, ARIMAResults):
            # if hasattr(model, 'arroots'):
              # unscaled_arima_train_x = trainScaler.inverse_transform(scaled_models_train_x)
                model = ARIMA(arima_data, 
                              order = utils.get_arima_model_order(model), 
                              seasonal_order = utils.get_arima_model_seasonal_order(model))
                model = model.fit()
            elif "keras" in str(type(model)):                                                                              
                model.fit(models_train_x,
                scaled_models_train_y,
                batch_size=batch_size,
                epochs=epochs,
                validation_data=(models_val_x, scaled_models_val_y),
                callbacks=models_callbacks,
                verbose=0)    
            else: 
                model.fit(models_train_x,
                scaled_models_train_y)
            return model
# dataset split: models_train | models_val | regr_train | regr_val | test 
    i = 0
    for model in self.models:
        if isinstance(model, ARIMA) or isinstance(model, ARIMAResultsWrapper)  or isinstance(model, ARIMAResults):
                data = arima_data
                model = model_fit(model, data)
                train_predictions = model.forecast(len(regr_train))

                data = data + list(unscaled_regr_train)
                model = model_fit(model, data)
                val_predictions = model.forecast(len(regr_val))

                data = data + list(unscaled_regr_val)
                model = model_fit(model, data)
                test_predictions = model.forecast(len(test))
                print(pd.DataFrame({'prediction' : test_predictions, '1' : test_y}))
                ensemble_train_x.append(train_predictions)
                ensemble_val_x.append(val_predictions)
                ensemble_test_x.append(test_predictions)
        elif fit_models:
            model = model_fit(model, 
                                arima_data = None, 
                                models_train_x = models_train_x, 
                                scaled_models_train_y = scaled_models_train_y, 
                                models_val_x = models_val_x, 
                                scaled_models_val_y = scaled_models_val_y)
            train_predictions = model.predict(regr_train_x)
            train_predictions = regr_trainScaler.inverse_transform(train_predictions).flatten()
            ensemble_train_x.append(train_predictions)
            model = model_fit(model, 
                                arima_data = None, 
                                models_train_x = regr_train_x, 
                                scaled_models_train_y = scaled_regr_train_y, 
                                models_val_x = models_val_x, 
                                scaled_models_val_y = scaled_models_val_y)
            
            val_predictions = model.predict(regr_val_x)
            val_predictions = regr_valScaler.inverse_transform(val_predictions).flatten()
            ensemble_val_x.append(val_predictions)
            model = model_fit(model, 
                                arima_data = None, 
                                models_train_x = models_val_x, 
                                scaled_models_train_y = scaled_models_val_y, 
                                models_val_x = regr_val_x, 
                                scaled_models_val_y = scaled_regr_val_y)
            
            test_predictions = model.predict(test_x)
            test_predictions = testScaler.inverse_transform(test_predictions).flatten()
            ensemble_test_x.append(test_predictions)
        else:
            train_predictions = model.predict(regr_train_x)
            train_predictions = regr_trainScaler.inverse_transform(train_predictions).flatten()
            ensemble_train_x.append(train_predictions)
            val_predictions = model.predict(regr_val_x)
            val_predictions = regr_valScaler.inverse_transform(val_predictions).flatten()
            ensemble_val_x.append(val_predictions)
            test_predictions = model.predict(test_x)
            test_predictions = testScaler.inverse_transform(test_predictions).flatten()
            ensemble_test_x.append(test_predictions)
               
        if metric.lower() == "mae":
            error = utils.get_mae(test_predictions, test_y)
            metrics.append(utils.get_mae(train_predictions, regr_train_y))
        elif metric.lower() == "rmse":
            error = utils.get_rmse(test_predictions, test_y)
            metrics.append(utils.get_rmse(train_predictions, regr_train_y))             
        elif metric.lower() == "mse":
            error = utils.get_mse(test_predictions, test_y)
            metrics.append(utils.get_mse(train_predictions, regr_train_y))
        elif metric.lower() == "mape":
            error = utils.get_mape(test_predictions, test_y)
            metrics.append(utils.get_mape(train_predictions, regr_train_y))
        elif metric.lower() == "coeff_determination" or metric.lower() == "determination":
            error = utils.get_coeff_determination(test_predictions, test_y)
            metrics.append(utils.get_coeff_determination(train_predictions, regr_train_y))
        print("model {} : {}, {} = {} \n".format(i, type(model), metric, error))
        i = i + 1

    if not(features is None):
        for f in features:
            f = np.array(f).flatten()
            ensemble_train_x.append(f[(models_val_num + look_back):regr_train_num])
            ensemble_test_x.append(f[(regr_val_num + look_back):])
            ensemble_val_x.append(f[(regr_train_num + look_back):regr_val_num])

            if metric.lower() == "mae":
                error = utils.get_mae(f[(regr_val_num + look_back):], test_y)
                metrics.append(error)
            elif metric.lower() == "rmse":
                error = utils.get_rmse(f[(regr_val_num + look_back):], test_y)
                metrics.append(error)             
            elif metric.lower() == "mse":
                error = utils.get_mse(f[(regr_val_num + look_back):], test_y)
                metrics.append(error)
            elif metric.lower() == "mape":
                error = utils.get_mape(f[(regr_val_num + look_back):], test_y)
                metrics.append(error)
            elif metric.lower() == "coeff_determination" or metric.lower() == "determination":
                error = utils.get_coeff_determination(f[(regr_val_num + look_back):], test_y)
                metrics.append(error)


    ensemble_train_x = list(zip(*ensemble_train_x))
    ensemble_val_x = list(zip(*ensemble_val_x))
    ensemble_test_x = list(zip(*ensemble_test_x))

    ensemble_train_x = np.array(ensemble_train_x)
    ensemble_val_x = np.array(ensemble_val_x)
    ensemble_test_x = np.array(ensemble_test_x)

    ensemble_val_x = np.reshape(ensemble_val_x,(-1,len(self.models) + len(features)) )
    ensemble_train_x = np.reshape(ensemble_train_x,(-1,len(self.models) + len(features)))
    ensemble_test_x = np.reshape(ensemble_test_x,(-1,len(self.models) + len(features)))

    # print("VAL")
    # print(regr_val_y)
    # print(ensemble_val_x)
    # print("test")
    # print(test_y)
    # print(ensemble_test_x)
    # print("train")
    # print(regr_train_y)  
    # print(ensemble_train_x)
    if self.regressor.lower() == "lgbm" or self.regressor.lower() == "lightgbm":
        if regr_params is None:
            if self.regr_params is None:

                # params = {'num_leaves': 62,
                #     'max_depth' : 6,
                #     'n_estimators': 500,
                #     'min_child_samples': 20,
                #     'learning_rate': 0.1,
                #     'subsample': 1,
                #     'colsample_bytree': 1,
                #     'snapshot_freq' : 1 ,
                #     'verbose' : -1}
               params = {'verbose': -1}
            else:
                params = self.regr_params
        else:
            params = regr_params

        regr = lgb.LGBMRegressor(**params)

        if not(early_stop is None) and isinstance(early_stop, int):
            earlystop = lgb.early_stopping(early_stop)
            regr = regr.fit(ensemble_train_x,
                            regr_train_y,
                            eval_set = (ensemble_val_x, regr_val_y),
                            callbacks = [earlystop])
        else:
            regr = regr.fit(ensemble_train_x,
                            regr_train_y,
                            eval_set = (ensemble_val_x, regr_val_y))
            
    elif self.regressor.lower() == "catboost":
        if regr_params is None:
            if self.regr_params is None:
                # params = {'iterations': 20,
                #         'depth': 6,
                #         'verbose' : 0}
               params = {'verbose': 0}
            else:
                params = self.regr_params
        else:
            params = regr_params

        regr = CatBoostRegressor(**params)

        if not(early_stop is None) and isinstance(early_stop, int):
            regr = regr.fit(ensemble_train_x,
                            regr_train_y,
                            eval_set = (ensemble_val_x, regr_val_y),
                            early_stopping_rounds = early_stop)
        else:
            regr = regr.fit(ensemble_train_x,
                            regr_train_y,
                            eval_set = (ensemble_val_x, regr_val_y))

    elif self.regressor.lower() == "mean":
        regr = meanRegressor()

    elif self.regressor.lower() == "wmean":
        invertedMetric = np.array([1/x for x in metrics])
        weights = invertedMetric/invertedMetric.sum()
        regr = wMeanRegressor(weights)
    else:
       raise Exception("Regressor is not supported")

    self.test_x = ensemble_test_x
    self.test_y = test_y
    self.model = regr
    
    return self.model


  def eval(self, test_x = None, test_y = None, max_plot = 150, testScaler = None, get = "mape", plot = "True", print_values = True, verbose = True, fig_size = (15,5)):
    """ 
    Same as TSEnsemble.utils.eval_model
    """
    if test_x is None:
      if self.test_x is None: 
        return Exception("Test dataset not found")
      test_x = self.test_x
      test_y = self.test_y

    return utils.eval_model(self.model, test_x, test_y, max_plot = max_plot, testScaler = testScaler, get = get, plot = plot, print_values = print_values, verbose = verbose, fig_size = fig_size)


  def add_model(self, models):
    self.models.append(models)
    
  def remove_model(self, model):
    self.models.remove(model)
    
  def forecast(self, dataset, n = 1, look_back = None, plot = True, datePlot = "date", dateStep = 1, fig_size = (10,10), features = []):
    """ 
    Out-of-sample forecast based on a given dataset
    """
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
    Scaler = MinMaxScaler(feature_range=(-1, 1))
    dataset = Scaler.fit_transform(dataset)
    dataset = dataset.tolist() 
    # Collect predictions of all models
    models_predictions = []
    for model in self.models:
      if isinstance(model, ARIMA) or isinstance(model, ARIMAResultsWrapper)  or isinstance(model, ARIMAResults): 
        model = ARIMA(Scaler.inverse_transform(dataset), 
                    order=utils.get_arima_model_order(model), 
                    seasonal_order = utils.get_arima_model_seasonal_order(model))
        model = model.fit()
        predictions = model.forecast(n)
        models_predictions.append(predictions)
      else:
        if look_back is None:
          s = utils.get_seasonality(model)
        else:
          s = look_back

        X = dataset[-s:]
        predictions = []
        # Predicts 1 future value based on last look_back values
        for i in range(n):
            fromX = s - i
            a = X[-fromX:] if fromX > 0 else []
            fromPredictions = min(i,s)
            a = a + predictions[-fromPredictions:]
            a = np.array(a).reshape(1,-1,1)
            prediction = model.predict(a, verbose = 0).tolist()
            predictions = predictions + prediction
        # Unscale predictions and add to list
        predictions = Scaler.inverse_transform(predictions).flatten().tolist()
        models_predictions.append(predictions)

    for f in features:
        f = np.array(f).flatten()
        models_predictions.append(f[:n])

    models_predictions = np.array(models_predictions).T.tolist()

    predictions = self.model.predict(models_predictions)

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
  
class meanRegressor:
  def predict(self, x):
     return np.mean(x, axis = 1)
  
class wMeanRegressor: 
  def __init__(self, weights = []):
     self.weights = weights
  def predict(self, x):
     return np.dot(x, self.weights)
  
  