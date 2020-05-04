# Combating Covid-19

## Introduction

The Novel Coronavirus has done some damage to us all in these recent few months. It is still going to haunt us for a few more years..... And God knows how many more of these "Pandemics" we will have by then. To Assess the the infections, deaths, recovery, etc of a pandemic. we have built an SEIR Model. This Repo currently is written and all data generated around it currently supports a Prediction Model of the Novel Coronairus in about 300 days from 4/05/2020 (4th March 2020).

Testing Conditions: Windows 10.0.0.18363, 8GB Ram, Python 3.8 and Pip 20.0.2

## Special Libraries
Networkx, Seirplus, Numpy, Pickle

To Install the above libraries:
```bash
pip install networkx seirplus numpy pickle
pip3 install networkx seirplus numpy pickle
```

Please Note: Don't use the pickle file extension if you are sharing it over the internet. Pickle is an Unencrypted file extension and can be easily tampered with. Since you will be loading the pickle file into your **Executable** python file. It can be potentially harmful.Use at your own risk.

## The SEIR Model
The SEIR Model is the simplest, accurate and least compute/memory intensive predictive algorithim that exists today to predict the effects of a so called **Pandemic** It is a mneumonic for Susceptible, Infectious, Exposed, Recovered Model. It can further be made a little more accurate if another S is added to account for "Re-Susceptiility" 

