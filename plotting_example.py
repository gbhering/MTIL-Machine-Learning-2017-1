# credits to Julia Evans
# jvns.ca/blog/2014/11/17/fun-with-machine-learning-logistic-regression/

# this example is moot since our data has more than two attributes...
# but still, may come to be useful so here it is --gab

from math import exp

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

n = 5000
a = 0.7

# this is utterly random data, in theory the two datasets would be 
dataset = pd.DataFrame({
    'panda': np.random.normal(0, 1, n),
    'elephant': np.random.normal(0, 1, n)
})

# also a random model function
x = np.random.sample(n)*dataset['panda'] - np.random.sample(n)*dataset['elephant']
# x = dataset['panda']*dataset['elephant']
# x = -1/3 * (dataset['panda'] +  dataset['elephant']**3)
# x = - 1/3 * (dataset['panda'] +  dataset['elephant'])

# logistic regression is here
probabilities = 1 / (1 + np.exp(-1 * x))

# the target function is also utterly random
# dataset['target'] = np.random.uniform(0,1,n) < probabilities
dataset['target'] = 0.5 < probabilities
print(dataset.target.value_counts())

plt.plot(
	dataset.where(dataset['target'] == True)['panda'],
	dataset.where(dataset['target'] == True)['elephant'],
	'b.', alpha=a, label='Positive')

plt.plot(
	dataset.where(dataset['target'] == False)['panda'],
	dataset.where(dataset['target'] == False)['elephant'],
	'c.', alpha=a, label='Negative')

plt.title("Distribution of observations")
plt.legend()
plt.axis([-4, 4, -4, 4])
plt.ylabel('panda')
plt.xlabel('elephant')
plt.grid(True)
plt.show()