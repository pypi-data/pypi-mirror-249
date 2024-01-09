import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import time
from TSEnsemble import utils
import pandas as pd
import matplotlib.pyplot as plt

def root_test(model, aic):
    """
    Check the roots of the new model, and set AIC to inf if the roots are
    near non-invertible. 
    """
    max_invroot = 0
    p, d, q = model.order
    P, D, Q, m = model.S

    if p + P > 0:
        max_invroot = max(0, *np.abs(1 / model.arroots))
    if q + Q > 0 and np.isfinite(aic):
        max_invroot = max(0, *np.abs(1 / model.maroots))

    if max_invroot > 0.99:
        aic = np.inf
    return aic

def auto_arima(dataset, 
               method = 'stepwise', 
               max_p = 3, 
               d = None, 
               max_q = 3, 
               season = None, 
               max_P = 3, 
               D = None, 
               max_Q = 3, 
               verbose = True, 
               train_size = None,
               train_split = None, 
               plot = True, 
               fig_size = (15,5),
               max_plot = 200):
    """
    Automatically find the best parameters for (S)AR(I)MA model 
    """

    if train_size is None and train_split is None:
        train_split = 0.9
    elif train_split is None and not(train_size is None):
        train_split = train_size

    if hasattr(dataset, 'values'):
        dataset = dataset.values
    
    if (np.isnan(dataset).any()):
        dataset = utils.interpolate_nan(dataset)

    # try to find correct d value
    is_stationary = utils.isStationaryArray(dataset, plot = False, verbose = False)
    if not(is_stationary) and d is None:
        for i in range(3):
                # check if differentiating i times makes data stationary
                if utils.isStationaryArray(np.diff(dataset.squeeze(), n = i + 1), plot = False, verbose = False):
                    d = i + 1
                    break
        if d is None:
            print("Cannot transform data to Stationary. Using ARIMA model would be inappropriate")
            d = 3
    elif d is None:
        d = 0
    if D is None:
       D = d     


    train_size = int(len(dataset) * train_split)
    train_data = dataset[:train_size]
    test_data = dataset[train_size:]
    train_data = list(np.concatenate(train_data).flat) 
    test_data = list(np.concatenate(test_data).flat) 


    if method == 'stepwise':
        model = stepwise_auto_arima(train_data, max_p = max_p, d = d, max_q = max_q, season = season, max_P = max_P, D = D, max_Q = max_Q)
    elif method == 'grid':
        model = grid_auto_arima(train_data, max_p = max_p, d = d, max_q = max_q, season = season, max_P = max_P, D = D, max_Q = max_Q)
    else:
        return "method should be grid or stepwise"

    predictions = model.forecast(len(test_data))

    if plot:
            plt.figure(figsize=fig_size)
            plt.plot(test_data[-max_plot:], label = "Actual")
            plt.plot(predictions[-max_plot:], label = "Prediction")               
            plt.ylabel('Values', fontsize=15)
            plt.legend()
            plt.show()

    if verbose == False:
        return model
    
    print(pd.DataFrame({'prediction' : predictions, 'actual' : test_data}))

    rmse = utils.get_rmse(predictions, test_data)
    mse = utils.get_mse(predictions, test_data)
    mae = utils.get_mae(predictions, test_data)
    mape = utils.get_mape(predictions, test_data)

    print("RMSE = {}, MSE = {}, MAE = {}, MAPE = {}".format(rmse, mse, mae, mape))

    return model
# evaluate combinations of p, d and q values for an ARIMA model
def grid_auto_arima(data, max_p = 3, d = None, max_q = 3, season = None, max_P = 3, D = None, max_Q = 3):
    """
    Evaluate combinations of p, d and q values for an ARIMA model using grid search
    """
    
    best_aic, best_model, = float("inf"), None
    if season is None:
        for p in range(0, max_p + 1):
            for q in range(0, max_q + 1):
                try:
                    if p == 0 and q == 0:
                        continue
                    model = model_arima(data, [p, d, q])
                    if model.aic < best_aic:
                        best_aic, best_model = model.aic, model
                except:
                    continue
        if d == 0:
            print('Best ARMA%s  AIC=%.3f' % (best_model, best_aic))
        else:
            print('Best ARIMA%s  AIC=%.3f' % (best_model, best_aic))
    else:
        for p in range(0, max_p + 1):
            for q in range(0, max_q + 1):
                for P in range(0, max_P + 1):
                    for Q in range(0, max_Q + 1):
                        try:
                            if p == 0 and q == 0:
                                continue
                            model = model_arima(data, (p, d, q), S = (P, D, Q, season))
                            if model.aic < best_aic:
                                best_aic, best_model = model.aic, model
                        except:
                                continue
        if d == 0 and D == 0:
            print('Best SARMA%s  AIC=%.3f' % (best_model.order, best_aic))
        else:
            print('Best SARIMA%s  AIC=%.3f' % (best_model.order, best_aic))
    return best_model

def stepwise_auto_arima(data, max_p = 3, d = None, max_q = 3, season = None, max_P = 3, D = None, max_Q = 3):
    """
    Stepwise approach to find the best parameters for (S)AR(I)MA model
    """

    best_model = [np.inf,[],[],None]

    def minAic(order):
        """
        Compare given parameters of model to the current best
        """
        nonlocal best_model
        model = model_arima(data, order)
        if model.aic < best_model[0]:
            best_model[0], best_model[1], best_model[3] = model.aic, order, model
        return 
    
    def minAicS(order, S):
        """
        Compare given parameters of model to the current best for Seasonal AR(I)MA
        """
        nonlocal best_model
        model = model_arima(data, order, S = S)
        if model.aic < best_model[0]:
            best_model  = [model.aic, model.order, model.S, model]
        return

        
    def findBestModel():
            """
            Clockwise cycle
            """
            nonlocal best_model
            new_order=best_model[1].copy()
            if new_order[0] > 0:
                new_order[0] = new_order[0] - 1
                minAic(new_order)
                if new_order == best_model[1]:
                    findBestModel()

            new_order = best_model[1].copy()

            if new_order[2] > 0:
                new_order[2] = new_order[2] - 1
                minAic(new_order)
                if new_order == best_model[1]:
                    findBestModel()

            new_order = best_model[1].copy()

            if new_order[0] + 1 <= max_p:
                new_order[0] = new_order[0] + 1
                minAic(new_order)
                if new_order == best_model[1]:
                    findBestModel()

            new_order = best_model[1].copy()

            if new_order[2] + 1 <= max_q:
                new_order[2] = new_order[2] + 1        
                minAic(new_order)
                if new_order == best_model[1]:
                    findBestModel()

            new_order = best_model[1].copy()
            
            if new_order[2] + 1 <= max_q and new_order[0] + 1 <= max_p:
                new_order[2] = new_order[2] + 1   
                new_order[0] = new_order[0] + 1      
                minAic(new_order)
                if new_order == best_model[1]:
                    findBestModel()

            new_order = best_model[1].copy()

            if new_order[2] - 1 > -1 and new_order[0] - 1 > -1:
                new_order[2] = new_order[2] - 1   
                new_order[0] = new_order[0] - 1      
                minAic(new_order)
                if new_order == best_model[1]:
                    findBestModel()

            new_order = best_model[1].copy()
            
            if new_order[2] - 1 > -1 and new_order[0] + 1 <= max_p:
                new_order[2] = new_order[2] - 1   
                new_order[0] = new_order[0] + 1      
                minAic(new_order)
                if new_order == best_model[1]:
                    findBestModel()

            new_order = best_model[1].copy()
            
            if new_order[0] - 1 > -1 and new_order[2] + 1 <= max_q:
                new_order[2] = new_order[2] + 1   
                new_order[0] = new_order[0] - 1      
                minAic(new_order)
                if new_order == best_model[1]:
                    findBestModel()

            new_order = best_model[1].copy()



            return
    
    def findBestModelS():
                """
                Clockwise cycle for seasonal model
                """
                nonlocal best_model
                new_order = best_model[1].copy()
                new_S = best_model[2].copy()

                # Change p, q, P, Q by +-1. If better model found, start over
                if new_order[0] > 0:
                    new_order[0] = new_order[0] - 1
                    if not([new_order, new_S] in used_configs):
                        minAicS(new_order, new_S)
                        used_configs.append([new_order, new_S])
                        if  best_model[1] == new_order and best_model[2] == new_S:
                            findBestModelS()

                new_order = best_model[1].copy()
                new_S = best_model[2].copy()    

                if new_order[2] > 0:
                    new_order[2] = new_order[2] - 1
                    if not([new_order, new_S] in used_configs):
                        minAicS(new_order, new_S)
                        used_configs.append([new_order, new_S])
                        if  best_model[1] == new_order and best_model[2] == new_S:
                            findBestModelS()

                new_order = best_model[1].copy()
                new_S = best_model[2].copy()

                if new_S[0] > 0:
                    new_S[0] = new_S[0] - 1 
                    if not([new_order, new_S] in used_configs):
                        minAicS(new_order, new_S)
                        used_configs.append([new_order, new_S])
                        if  best_model[1] == new_order and best_model[2] == new_S:
                            findBestModelS()

                new_order = best_model[1].copy()
                new_S = best_model[2].copy()

                if new_S[2] > 0:
                    new_S[2] = new_S[2] - 1
                    if not([new_order, new_S] in used_configs):
                        minAicS(new_order, new_S)
                        used_configs.append([new_order, new_S])
                        if  best_model[1] == new_order and best_model[2] == new_S:
                            findBestModelS()

                new_order = best_model[1].copy()
                new_S = best_model[2].copy()


                if new_order[0] + 1 <= max_p:
                    new_order[0] = new_order[0] + 1
                    if not([new_order, new_S] in used_configs):
                        minAicS(new_order, new_S)
                        used_configs.append([new_order, new_S])
                        if  best_model[1] == new_order and best_model[2] == new_S:
                            findBestModelS()

                new_order = best_model[1].copy()
                new_S = best_model[2].copy()

                if new_order[2] + 1 <= max_q:
                    new_order[2] = new_order[2] + 1
                    if not([new_order, new_S] in used_configs):
                        minAicS(new_order, new_S)
                        used_configs.append([new_order, new_S])
                        if  best_model[1] == new_order and best_model[2] == new_S:
                            findBestModelS()

                new_order = best_model[1].copy()
                new_S = best_model[2].copy()

                if new_S[0] + 1 <= max_P:
                    new_S[0] = new_S[0] + 1
                    if not([new_order, new_S] in used_configs):
                        minAicS(new_order, new_S)
                        used_configs.append([new_order, new_S])
                        if  best_model[1] == new_order and best_model[2] == new_S:
                            findBestModelS()

                new_order = best_model[1].copy()
                new_S = best_model[2].copy()

                if new_S[2] + 1 <= max_Q:
                    new_S[2] = new_S[2] + 1
                    if not([new_order, new_S] in used_configs):
                        minAicS(new_order, new_S)
                        used_configs.append([new_order, new_S])
                        if  best_model[1] == new_order and best_model[2] == new_S:
                            findBestModelS()

                new_order = best_model[1].copy()
                new_S = best_model[2].copy()
                
                if new_order[2] + 1 <= max_q and new_order[0] + 1 <= max_p:
                    new_order[2] = new_order[2] + 1   
                    new_order[0] = new_order[0] + 1      
                    if not([new_order, new_S] in used_configs):
                        minAicS(new_order, new_S)
                        used_configs.append([new_order, new_S])
                        if  best_model[1] == new_order and best_model[2] == new_S:
                            findBestModelS()

                new_order = best_model[1].copy()
                new_S = best_model[2].copy()

                if new_order[2] - 1 > -1 and new_order[0] - 1 > -1:
                    new_order[2] = new_order[2] - 1   
                    new_order[0] = new_order[0] - 1      
                    if not([new_order, new_S] in used_configs):
                        minAicS(new_order, new_S)
                        used_configs.append([new_order, new_S])
                        if  best_model[1] == new_order and best_model[2] == new_S:
                            findBestModelS()

                new_order = best_model[1].copy()
                new_S = best_model[2].copy()

                if new_S[2] + 1 <= max_Q and new_S[0] + 1 <= max_P:
                    new_S[2] = new_S[2] + 1   
                    new_S[0] = new_S[0] + 1   
                    if not([new_order, new_S] in used_configs):
                        minAicS(new_order, new_S)
                        used_configs.append([new_order, new_S])
                        if  best_model[1] == new_order and best_model[2] == new_S:
                            findBestModelS()

                new_order = best_model[1].copy()
                new_S = best_model[2].copy()

                if new_S[2] - 1 > -1 and new_S[0] - 1 > -1:
                    new_S[2] = new_S[2] - 1   
                    new_S[0] = new_S[0] - 1  
                    if not([new_order, new_S] in used_configs):
                        minAicS(new_order, new_S)
                        used_configs.append([new_order, new_S])
                        if  best_model[1] == new_order and best_model[2] == new_S:
                            findBestModelS()

                new_order = best_model[1].copy()
                new_S = best_model[2].copy()

                if new_S[2] - 1 > -1 and new_S[0] + 1 <= max_P:
                    new_S[2] = new_S[2] - 1   
                    new_S[0] = new_S[0] + 1  
                    if not([new_order, new_S] in used_configs):
                        minAicS(new_order, new_S)
                        used_configs.append([new_order, new_S])
                        if  best_model[1] == new_order and best_model[2] == new_S:
                            findBestModelS()

                new_order = best_model[1].copy()
                new_S = best_model[2].copy()

                if new_S[0] - 1 > -1 and new_S[2] + 1 <= max_Q:
                    new_S[2] = new_S[2] + 1   
                    new_S[0] = new_S[0] - 1  
                    if not([new_order, new_S] in used_configs):
                        minAicS(new_order, new_S)
                        used_configs.append([new_order, new_S])
                        if  best_model[1] == new_order and best_model[2] == new_S:
                            findBestModelS()

                new_order = best_model[1].copy()
                new_S = best_model[2].copy()

                return 
    

    start = time.process_time()  # Start Timer
    if season is None:
        # initial parameters for clockwise search
        minAic([2, d, 2])
        minAic([0, d, 0])
        minAic([1, d, 0])
        minAic([0, d, 1])
        findBestModel()  # clockwise recursive cycle
        end = time.process_time() - start  # End Timer
        print("Best model: %s, AIC: %.3f" % (best_model[1], best_model[0]))
        print("Total time: ", end)
        return best_model[3]
    else:
        # initial parameters for clockwise search for seasonal data
        p = min(2, max_p)
        q = min(2, max_q)
        P = min(1, max_P)
        Q = min(1, max_Q)

        minAicS([p, d, q], [P, D, Q, season])
        minAicS([0, d, 0], [0, D, 0, season])   
        minAicS([1, d, 0], [1, D, 0, season])
        minAicS([0, d, 1], [0, D, 1, season])

        # storing configs to avoid evaluating same set of parameters
        used_configs = [ [[p, d, q], [P, D, Q, season]], [[0, d, 0], [0, D, 0, season]], [[1, D, 0, season], [1, d, 0]], [[0, D, 1, season], [0, d, 1]]]
        findBestModelS()   # clockwise recursive cycle
        end = time.process_time() - start   # End Timer

        print("Best model: %s %s, AIC: %.3f" % (best_model[1], best_model[2], best_model[0]))
        print("Total time: ", end)

        return best_model[3]
    

def model_arima(train_data, order, S = None):
    """
    Evaluate an ARIMA model for a given order (p,d,q)(P,D,Q,S) and return a model
    """
    import warnings
    from statsmodels.tools.sm_exceptions import ConvergenceWarning
    warnings.simplefilter('ignore', ConvergenceWarning)
    warnings.simplefilter('ignore', UserWarning)
    start = time.process_time()
    if S:
        # create and fit model, assign order and seasonal order to model
        model = ARIMA(train_data, order=order, seasonal_order = S)
        model = model.fit() 
        model.order = order
        model.S = S
        # if root_test fails, set AIC to inf
        model.aic = root_test(model, model.aic)
        end = time.process_time() - start  # End Timer

        if order[1] == 0:
            print('SARMA%s %s AIC:%.3f  Time_Taken:%.3f' % (order, S, model.aic, end))
        else:
            print('SARIMA%s %s AIC:%.3f  Time_Taken:%.3f' % (order, S, model.aic, end))  
        return model
    else:
        # create and fit model, assign order and seasonal order to model
        model = ARIMA(train_data, order=order)
        model = model.fit() 
        model.order = order
        model.S = [0,0,0,0]
        # if root_test fails, set AIC to inf
        model.aic = root_test(model, model.aic)
        end = time.process_time() - start  # End Timer

        if order[1] == 0:
            print('ARMA%s AIC:%.3f  Time_Taken:%.3f' % (order, model.aic, end))
        else:
            print('ARIMA%s AIC:%.3f  Time_Taken:%.3f' % (order, model.aic, end))
        return model

def make_arima(dataset, order, seasonal_order = None, train_size = 0.9, test_size = None, fig_size = (15,5), plot = True, verbose = True, max_plot = 200):
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

    # split into train and test sets
    train_num = int(len(dataset) * train_size)
    train_x, test_data = dataset[0:train_num], dataset[train_num:]
    model = ARIMA(train_x, order = order, seasonal_order = seasonal_order)
    model = model.fit()
    print("AIC: ", model.aic)

    predictions = model.forecast(len(test_data))
    test_data = test_data.flatten()
    if plot:
            plt.figure(figsize=fig_size)
            plt.plot(test_data[-max_plot:], label = "Actual")
            plt.plot(predictions[-max_plot:], label = "Prediction")               
            plt.ylabel('Values', fontsize=15)
            plt.legend()
            plt.show()

    if verbose == False:
        return model
    print(pd.DataFrame({'prediction' : predictions, 'actual' : test_data.flatten()}))

    rmse = utils.get_rmse(predictions, test_data)
    mse = utils.get_mse(predictions, test_data)
    mae = utils.get_mae(predictions, test_data)
    mape = utils.get_mape(predictions, test_data)

    print("RMSE = {}, MSE = {}, MAE = {}, MAPE = {}".format(rmse, mse, mae, mape))
    return model
    
