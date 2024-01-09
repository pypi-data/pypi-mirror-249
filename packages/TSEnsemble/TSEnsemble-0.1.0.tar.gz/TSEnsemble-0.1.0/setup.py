from setuptools import find_packages, setup

setup(
    name='TSEnsemble',
    packages=find_packages(include=['TSEnsemble']),
    version='0.1.0',
    description='A Python library for times series forecasting, which uses an ensemble of methods, including SARIMA and deep learning models',
    author='Viktor Astakhov',
    install_requires=[ # 'pytest-runner', 
                    'numpy', 
                    'pandas', 
                    'keras',
                    'sklearn',
                    'statsmodels', 
                    'matplotlib', 
                    'lightgbm',
                    'catboost'],
    setup_requires=[
                   ]
)

