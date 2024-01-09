# TSEnsemble

Automatically build deep learning and ARIMA models and use them for an ensemble of models.
Library has different tools for time series analysis and has a simple architecture to use.


## Installation

Install TSEnsemble with pip. Run the command below in terminal:

```bash
  pip install TSEnsemble
```
    
## Usage
In this example we will run ensemble of SARIMA, cnn, lstm and transformer models using weighted means of models. Weights are given based on the error metric, in our case it is RMSE:
### Firstly, import TSEnsemble modules:
```Python
from TSEnsemble import nn, arima, utils
from TSEnsemble.ensemble import Ensemble
```
### Then, load dataset from .csv file and plot ACF and Seasonal decompose.
To load dataset use function ts_from_csv: \
**column** : int or str - index or name of a column, that has time series values.\
**index** : int or str - index or name of a column, that has time series timestamps.\

Autocorellation function can help us to identify seasonality of a model.\
Decompose function splits time series into trend, season and residuals parts.

```Python
path = "C:\\Users\\Viktor\\MyLibrary\\GlobalTemperatures.csv"
dataset = utils.ts_from_csv(path, column = 1, index = 0)
from statsmodels.graphics.tsaplots import plot_acf
utils.plot_acf(path, lags = 26)
utils.plot_decompose(path, period = 12)
```
### Then, generate our models with preferred parameters.
You can use make_(model_name) functions with dataset and train parameters to find out what parameters fit your model best.

```Python
ar = arima.auto_arima(dataset,
                            method = 'stepwise',
                            season = 12,
                            max_p = 3,
                            max_q = 3,
                            max_Q = 3,
                            max_P = 3,
                            train_split = 0.8,
                            plot = True)

transformer = nn.generate_transformer(
                    look_back = 12,
                    horizon = 1,
                    n_features = 1,
                    num_transformer_blocks = 4,
                    dropout = 0.25, 
                    head_size = 256, 
                    num_heads = 4, 
                    ff_dim = 4,
                    mlp_units=[128],
                    mlp_dropout=0.4)

lstm = nn.generate_rnn(look_back = 12,
                    hidden_layers = 1,
                    units = 64,
                    type = "LSTM",
                    dropout = 0.0)

cnn = nn.generate_cnn(look_back = 12,
                hidden_layers = 3,
                kernel_size = 2,
                filters = 64,
                dilation_rate = 1,
                dilation_mode = "multiplicative")
```
### Then, create Ensemble object, fit and evaluate created model.
Ensemble object initialization parameters:\
**models** : list of model objects.\
**regressor**: str, type of a regressor. Supported: 'mean', 'wmean', 'catboost', 'lightgbm'.\

Fit parameters:\
**dataset**: mandatory, dataset, used to train and test model.\
**train_size**: float from 0 to 1, part of dataset, used for training models.\
**look_back**: int, amount of input values. Not important, function will detect look_back without this parameter. Only same look_back for all NN models is supported right now.\
**val_size**: float from 0 to 1, part of training data used to validate models. Use models_val_size and regr_val_size to set different validation size for models and metamodel.\
**train_models_size**: float from 0 to 1, part of training data used to train models.\
**epochs**: int, amount of iterations of NN models through whole training data.\
**batch_size**: int, the number of samples that will be propagated through the network\
**metric**: str, metric used for weighting models. Supproted: mae, rmse, mse, mape, coeff_determination.
```Python
ensemble_model = Ensemble(models = [ar, cnn, lstm, transformer], regressor = 'wmean')
ensemble_model.fit(dataset, train_size = 0.8, look_back = 12, val_size = 0.2, train_models_size = 0.7, epochs = 20, batch_size = 16, metric = "rmse")
ensemble_model.eval(get="rmse")
```
### Lastly, use models to forecast future values of a dataset.
Parameters:\
**model**: mandatory, model object.\
**dataset**: mandatory, dataset used to train and test model.\
**n**: int, number of values to forecast.\
**fig_size**: tuple of 2 ints, size of a plot.
```Python
ensemble_model.forecast(dataset, 12, fig_size = (5,5))
utils.model_forecast(ar, dataset, 12, fig_size = (5,5))
```

## Requirements
Numpy, pandas, keras, sklearn, statsmodels, matplotlib, lightgbm, catboost.
## License
MIT License.