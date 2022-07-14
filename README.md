# Burn-up to massive
Calculates average [burn-up](https://en.wikipedia.org/wiki/Burnup) for each fuel assembly in research reactor [IR-8](http://kcsni.nrcki.ru/pages/main/IR8/index.shtml) and predicts reactivity margin.<div>
Since 2009, computational support for the operation of the reactor, as well as experiments on it, has been carried out using the [MCU program](https://mcuproject.ru/etlstp.html), which implements the Monte Carlo method. Calculation of 1 state of reactor using Monte Carlo method takes about 1-2 days, so there need to create regression model for operative estimation of reactivity margin. <div>
[file_extracters.py](https://github.com/KruglikovAnton/burn-up-to-massive/blob/master/file_extracters.py) contains functions for extracting data from input and output files of MCU programm.<div>
[interface_with_tkinter.py](https://github.com/KruglikovAnton/burn-up-to-massive/blob/master/interface_with_tkinter.py) contains class for interface app creation.<div>
In [reactivity_margin_prediction.py](https://github.com/KruglikovAnton/burn-up-to-massive/blob/master/reactivity_margin_prediction.py) a dataframe with data is formed by extracting information from the calculation files starting from 2015.<div>
[Building_regression_model.ipynb](https://github.com/KruglikovAnton/burn-up-to-massive/blob/master/Building_regression_model.ipynb) contains results of testing diffrent regression models. 
All the needed data you can find here.
