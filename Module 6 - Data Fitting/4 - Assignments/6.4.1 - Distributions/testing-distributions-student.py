import numpy as np
from scipy.stats import norm, expon
import matplotlib
import matplotlib.pyplot as plt
import platform

# a fix for Dr. Forsyth's computer
# https://stackoverflow.com/questions/56013105/matplotlib-plot-window-is-white-blank-without-showing-any-image
if platform.system() == 'Darwin':
    matplotlib.use('MacOSX')

"""
Step #1: Generate a Simple Distribution
"""

# desired average of normal distribution
desired_mu = 5

# desired standard deviation
desired_std = 12

# number of samples to take
num_samples = 1000

# generate those samples with numpy
normal_samples = np.random.normal(loc=desired_mu, scale=desired_std, size=num_samples)

"""
Step #2: Find the Mean and Standard Deviation of the Random Sample
"""
sample_mean = -1
sample_std_dev = -1

"""
Step #3: Generate the x and y points for the plot for a normal distribution
"""

# Hint: Remember the functions described in the examples, choose an appropriate range for x
x = -1
y = -1

"""
Step #4: Generate a plot for the Fitted Normal Distribution, include a title and axis labels
"""

# Your Code Here #

"""
Step 5: Compare your Fit against the true data
"""

# Don't Edit This Code #
x_correct = np.linspace(start=-31, stop=41, num=10000)
y_correct = norm.pdf(x_correct, loc=desired_mu, scale=desired_std)
plt.plot(x_correct, y_correct, label='Ideal Normal')

# include a legend
plt.legend()

# show the plot
plt.show()

"""
Step #6: Generate an exponential distribution
"""

# Don't edit this code #
desired_lambda = 0.4
desired_beta = 1 / desired_lambda
num_samples = 25
exponential_samples = np.random.exponential(scale=desired_beta, size=num_samples)

"""
Step #7: Create an Exponential Fit and pull out the Beta value
"""

# Hint: Use the appropriate function for Exponential Fit
(fit_loc, fit_scale) = None, None

# pull out beta from the fitted distribution
fit_beta = -1

"""
Step #8: Generate x and y from the Exponential Fit
"""

# Hint: Remember the functions described in the examples, choose an appropriate range for x
exp_x = -1
exp_y = -1

"""
Step #9: Generate a plot for the Fitted Exponential Distribution, include a title and axis labels
"""

# Your Code Here #

"""
Step #10: Compare your Fit against the true data
"""

# Don't Edit This Code #
exp_correct_x = np.linspace(start=0, stop=50, num=10000)
exp_correct_y = expon.pdf(exp_correct_x, scale=desired_beta)
plt.plot(exp_correct_x, exp_correct_y, label='Ideal Exponential')

# include a legend
plt.legend()

# show the plot
plt.show()

