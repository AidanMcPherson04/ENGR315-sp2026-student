import sys

import numpy as np
from scipy.stats import norm, chisquare
from numpy.random import lognormal
import matplotlib.pyplot as plt

"""
Example #1:
Replicating work from here: http://www.stat.yale.edu/Courses/1997-98/101/chigf.htm
"""

# load set of observation data
observations = np.loadtxt('yale-randoms.txt')

# bin the examples
bins = np.linspace(-2, 2, 9)  # Create 10 bins

# Trick from StackExchange to add infinite on each end
# https://stackoverflow.com/questions/11633874/numpy-use-bins-with-infinite-range
bins = np.r_[-np.inf, bins, np.inf]

# place observations into bins
observed_counts, observed_edges = np.histogram(observations, bins=bins, density=False)

# generate number of expected observations based upon distribution PDF
# This is the only working and helpful thing that ChatGPT ever generated about this problem/approach
expected_mu = 0
expected_std = 1

# CDF difference gives probabilities for each bin. Provided probability of
# value being within each bin. This is the only helpful piece of ChatGPT code ever.
expected_prob = np.diff(norm.cdf(bins, loc=expected_mu, scale=expected_std))

# Expected frequency for each bin
expected_counts = expected_prob * len(observations)

# Conduct chi2 test
# Reduce the degrees of freedom as the normal distribution has two parameters
(chi_stat, p_value) = chisquare(f_obs=observed_counts, f_exp=expected_counts, ddof=2)
print('Chi2 stat: ', chi_stat, 'p-value: ', p_value)

alpha = 0.05
if p_value < alpha:
    print('Reject null hypothesis. Counts are not equal.')
else:
    print('Accept null hypothesis. Counts are equal')
