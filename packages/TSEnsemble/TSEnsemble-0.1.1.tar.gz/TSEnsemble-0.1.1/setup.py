from setuptools import find_packages, setup

setup(
    name = 'TSEnsemble',
    packages = find_packages(include=['TSEnsemble']),
    version = '0.1.1',
    url = 'https://github.com/Fabulotus/TSEnsemble/tree/main',
    description = 'A Python library for times series forecasting, which uses an ensemble of methods, including SARIMA and deep learning models',
    long_description = 'Automatically build deep learning and ARIMA models and use them for an ensemble of models. Library has different tools for time series analysis and has a simple architecture to use.',
    author='Viktor Astakhov',
    install_requires = [ # 'pytest-runner',
                    'numpy', 
                    'pandas', 
                    'keras',
                    'sklearn',
                    'statsmodels', 
                    'matplotlib', 
                    'lightgbm',
                    'catboost']
)

