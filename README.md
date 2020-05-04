# Combating Covid-19

## Introduction

The Novel Coronavirus has done some damage to us all in these recent few months. It is still going to haunt us for a few more years..... And God knows how many more of these "Pandemics" we will have by then. To Assess the the infections, deaths, recovery, etc of a pandemic. we have built an SEIR Model. This Repo currently is written and all data generated around it currently supports a Prediction Model of the Novel Coronairus in about 300 days from 4/05/2020 (4th March 2020).

Testing Conditions: Windows 10.0.0.18363, 8GB Ram, Python 3.8 and Pip 20.0.2

## Special Libraries
Networkx, Seirplus, Numpy, Pickle

To Install the above libraries:
```Bash
pip install networkx seirplus numpy pickle
pip3 install networkx seirplus numpy pickle
```

Please Note: Don't use the pickle file extension if you are sharing it over the internet. Pickle is an Unencrypted file extension and can be easily tampered with. Since you will be loading the pickle file into your **Executable** python file. It can be potentially harmful.Use at your own risk.

## The SEIR Model
The SEIR Model is the simplest, accurate and least compute/memory intensive predictive algorithim that exists today to predict the effects of a so called **Pandemic** It is a mneumonic for Susceptible, Infectious, Exposed, Recovered Model. It can further be made a little more accurate if another S is added to account for "Re-Susceptiility" 

![SEIR MODEL](https://github.com/ryansmcgee/seirsplus/raw/master/images/SEIRS_diagram.png)

The rates of transition between the states are given by the parameters:

β: rate of transmission (transmissions per S-I contact per time)
σ: rate of progression (inverse of incubation period)
γ: rate of recovery (inverse of infectious period)
ξ: rate of re-susceptibility (inverse of temporary immunity period; 0 if permanent immunity)
μI: rate of mortality from the disease (deaths per infectious individual per time)

In this Python codoe we are use the first three params. The rest are self evoloving. It is upto you to change it.

## Using the Code
Step 1: Edit hyperparams.py
Step 2: Run episim.py
Step 3: Use The Generated files as you wish

```Python
S = model.numS      # time series of S counts
E = model.numE      # time series of E counts
I = model.numI      # time series of I counts
D_E = model.numD_E    # time series of D_E counts
D_I = model.numD_I    # time series of D_I counts
R = model.numR      # time series of R counts
F = model.numF      # time series of F counts

t = model.tseries   # time values corresponding to the above time series

G_normal     = model.G    # interaction network graph
G_quarantine = model.Q    # quarantine interaction network graph

beta = model.beta   # value of beta parameter (or list of beta values for each node if using network model)
# similar for other parameters
```

