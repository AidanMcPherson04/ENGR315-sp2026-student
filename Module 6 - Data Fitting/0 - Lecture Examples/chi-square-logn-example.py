import sys

import numpy as np
from scipy.stats import norm, chisquare
from numpy.random import lognormal
import matplotlib.pyplot as plt

"""
Example #2:
Sample the lognormal distribution and see if we fit
"""

# Step 1: Setup bins
logn_bins = np.linspace(0, 2, 9)  # Create 9 bins evenly spaced between 0 and 2

# tack infinity on the last bin
logn_bins = np.r_[logn_bins, np.inf]

# Step 2: Generate Expected counts from known distribution
logn_mu = 0.5
logn_std = 0.5
logn_samples = 50

logn_expected_prob = np.diff(lognormal.cdf(bins, loc=logn_mu, scale=logn_samples))

# Expected frequency for each bin
expected_counts = expected_prob * len(logn_samples)

# Step 3: Generate some "observed" data by randomly sampling the target distribution
observed = lognormal(mean=logn_mu, sigma=logn_samples, size=logn_samples)

observed_counts, observed_edges = np.histogram(observations, bins=logn_bins, density=False)