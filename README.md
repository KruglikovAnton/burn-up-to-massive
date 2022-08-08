# Burn-up to massive
Calculates average [burn-up](https://en.wikipedia.org/wiki/Burnup) for each fuel assembly in research reactor [IR-8](http://kcsni.nrcki.ru/pages/main/IR8/index.shtml) and predicts reactivity margin.<div>
Since 2009, computational support for the operation of the reactor, as well as experiments on it, has been carried out using the [MCU program](https://mcuproject.ru/etlstp.html), which implements the Monte Carlo method. Calculation of 1 state of reactor using Monte Carlo method takes about 1-2 days, so there is need to create regression model for operative estimation of reactivity margin. <div>
[file_extracters.py](https://github.com/KruglikovAnton/burn-up-to-massive/blob/master/file_extracters.py) contains functions for extracting data from input and output files of MCU programm.<div>
[interface_with_tkinter.py](https://github.com/KruglikovAnton/burn-up-to-massive/blob/master/interface_with_tkinter.py) contains class for interface app creation.<div>
In [reactivity_margin_prediction.py](https://github.com/KruglikovAnton/burn-up-to-massive/blob/master/reactivity_margin_prediction.py) a dataframe with data is formed by extracting information from the calculation files starting from 2015.<div>
[Building_regression_model.ipynb](https://github.com/KruglikovAnton/burn-up-to-massive/blob/master/Building_regression_model.ipynb) contains results of testing diffrent regression models. <div>
File .exe, created via pyinstaller (probably works in windows 10 only), some examples of input files and also 2 csv file that used in Building_regression_model.ipynb you can find [here](https://drive.google.com/drive/folders/1yNO_Za8HW0RppgdwNVR3oqgTsxKt1bG2?usp=sharing).

The final interface looks like:<div>
<div align="center">
  <img src="https://github.com/KruglikovAnton/burn-up-to-massive/blob/master/pictures/interface.png">
</div>
<div>
After calculation result appears with picture:
<div align="center">
  <img src=https://github.com/KruglikovAnton/burn-up-to-massive/blob/master/pictures/Figure_1.png>
</div>
You can see negative values of -0.2 because the reference uranium loadings for all fuel assemblies were used in the calculation, in fact the burnup in these cells is 0.0.
