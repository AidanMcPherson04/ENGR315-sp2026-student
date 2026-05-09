import pandas as pd
import numpy as np
from scipy.stats import norm, chisquare, ttest_ind, ttest_1samp
import matplotlib.pyplot as plt

"""
Preamble: Load data from source CSV file
"""
##Note, I changed the path to the data file to fit my code.
##Original path had "../../" at beginning
path_to_datafile = "./data/drop-jump/all_participant_data_rsi.csv"

data = pd.read_csv(path_to_datafile)

"""
Question 1: Load the force plate and acceleration based RSI data for all participants. Map each data set (accel and FP)
to a normal distribution. Clearly report the distribution parameters (mu and std) and generate a graph two each curve's 
probability distribution function. Include appropriate labels, titles, and legends.
"""
print('-----Question 1-----')

########################################Force Plate
##Load the force plate data
force_plate_rsi = data['force_plate_rsi'].dropna()

##Fit the data to a normal distribution
mu_fp, std_fp = norm.fit(force_plate_rsi)
print('Force Plate RSI Distribution Parameters: mu =', mu_fp,', std =', std_fp)

##Plot the data and the fitted distribution
plt.figure()
plt.plot(np.linspace(force_plate_rsi.min(), force_plate_rsi.max(), 100),
          norm.pdf(np.linspace(force_plate_rsi.min(), force_plate_rsi.max(), 100),
                    mu_fp, std_fp), 'r-', label='Fitted Distribution')
plt.xlabel('RSI')
plt.ylabel('Probability Density')
plt.title('Force Plate RSI Distribution')
plt.legend()

##Save and Show plot - Comment/Uncomment as necessary
plt.savefig('AMcP_ENGR315Exam2_force_plate_rsi_distribution.png')
##plt.show()


########################################Acceleration
##Load the acceleration data
accel_rsi = data['accelerometer_rsi'].dropna()

##Fit the data to a normal distribution
mu_accel, std_accel = norm.fit(accel_rsi)
print('Acceleration RSI Distribution Parameters: mu =', mu_accel,', std =', std_accel)

##Plot the data and the fitted distribution
plt.figure()
plt.plot(np.linspace(accel_rsi.min(), accel_rsi.max(), 100),
          norm.pdf(np.linspace(accel_rsi.min(), accel_rsi.max(), 100),
                    mu_accel, std_accel), 'r-', label='Fitted Distribution')
plt.xlabel('RSI')
plt.ylabel('Probability Density')
plt.title('Acceleration RSI Distribution')
plt.legend()

##Save and Show plot - Comment/Uncomment as necessary
plt.savefig('AMcP_ENGR315Exam2_accel_rsi_distribution.png')
##plt.show()

########################################
##Plot both distributions on the same graph with appropriate labels, titles, and legends
plt.figure()
plt.plot(np.linspace(force_plate_rsi.min(), force_plate_rsi.max(), 100),
            norm.pdf(np.linspace(force_plate_rsi.min(), force_plate_rsi.max(), 100),
                      mu_fp, std_fp), 'r-', label='Force Plate Fitted Distribution')
plt.plot(np.linspace(accel_rsi.min(), accel_rsi.max(), 100),
            norm.pdf(np.linspace(accel_rsi.min(), accel_rsi.max(), 100),
                      mu_accel, std_accel), 'b-', label='Acceleration Fitted Distribution')
plt.xlabel('RSI')
plt.ylabel('Probability Density')
plt.title('Force Plate and Acceleration RSI Distributions')
plt.legend()

##Save and Show plot - Comment/Uncomment as necessary
plt.savefig('AMcP_ENGR315Exam2_rsi_distributions_comparison.png')
##plt.show()

"""
Question 2: Conduct a Chi2 Goodness of Fit Test for each dataset to test whether the data is a good fit
for the derived normal distribution. Clearly print out the p-value, chi2 stat, and an indication of whether it is 
a fit or not. Do this for both acceleration and force plate distributions. It is suggested to generate 9 bins between 
[0,2), add append -inf and +inf to both ends of the bins. An alpha=0.05 is suitable for these tests.
"""
print('\n\n-----Question 2-----')
alpha = 0.05
"""
Acceleration
"""
##Define bins
bins_accel = np.linspace(0, 2, 10) 
bins_accel = np.r_[-np.inf, bins_accel, np.inf]

##Place values into bins
observed_counts_accel, observed_edges_accel = np.histogram(accel_rsi, bins=bins_accel, density=False)

##Define Expectated distribution parameters, same as above
expected_mu_accel = mu_accel
expected_std_accel = std_accel

# CDF difference gives probabilities for each bin. Provided probability of
expected_prob_accel = np.diff(norm.cdf(bins_accel, loc=expected_mu_accel, scale=expected_std_accel))

# Expected frequency for each bin
expected_counts_accel = expected_prob_accel * len(accel_rsi)

##Conduct the chi2 test
(chi2_stat_accel, p_value_accel) = chisquare(f_obs=observed_counts_accel, f_exp=expected_counts_accel, ddof=0)

##Print Resulta
print('Acceleration RSI Chi2 stat: ', chi2_stat_accel, 'p-value: ', p_value_accel)

##Check Null Hypothesis
if p_value_accel < alpha:
    print(p_value_accel,'<',alpha,': It is not a good fit.')
else:
    print(p_value_accel,'>',alpha,': It is a good fit.')

"""
Force Plate
"""
#Define bins
bins_fp = np.linspace(0, 2, 10)
bins_fp = np.r_[-np.inf, bins_fp, np.inf] 

##Place values into bins
observed_counts_fp, observed_edges_fp = np.histogram(force_plate_rsi, bins=bins_fp, density=False)

##Define Expectated distribution parameters, same as above
expected_mu_fp = mu_fp
expected_std_fp = std_fp

# CDF difference gives probabilities for each bin. Provided probability of
expected_prob_fp = np.diff(norm.cdf(bins_fp, loc=expected_mu_fp, scale=expected_std_fp))

# Expected frequency for each bin
expected_counts_fp = expected_prob_fp * len(force_plate_rsi)

##Conduct the chi2 test
(chi2_stat_fp, p_value_fp) = chisquare(f_obs=observed_counts_fp, f_exp=expected_counts_fp, ddof=0)

##Print results
print('Force Plate RSI Chi2 stat: ', chi2_stat_fp, 'p-value: ', p_value_fp)

##Check Null Hypothesis
if p_value_fp < alpha:
    print(p_value_fp,'<',alpha,': It is not a good fit.')
else:
    print(p_value_fp,'>',alpha,': It is a good fit.')


"""
Question 3: Perform a t-test to determine whether the RSI means for the acceleration and force plate data are equivalent 
or not. Clearly report the p-value for the t-test and make a clear determination as to whether they are equal or not.
An alpha=0.05 is suitable for these tests.
"""
print('\n\n-----Question 3-----')

##This is a two sample t-test
t_stat, p_value_ttest = ttest_ind(accel_rsi, force_plate_rsi, equal_var=False)


##Print results
print('T-test stat: ', t_stat, 'p-value: ', p_value_ttest)

##Check Null Hypothesis
if p_value_ttest < alpha:
    print(p_value_ttest,'<',alpha,': The means are not equal.')
else:
    print(p_value_ttest,'>',alpha,': The means are equal.')

"""
Question 4: Calculate the RSI Error for the dataset where error is expressed as the difference between the 
Force Plate RSI measurement and the Accelerometer RSI measurement. Fit this error distribution to a normal curve and 
plot a histogram of the data on the same plot showing the fitted normal curve. Include appropriate labels, titles, and 
legends. The default binning approach from matplot lib with 16 bins is sufficient.
"""

##Load in Percent error
percent_error = data['percent_error'].dropna()

##Fit the data into normal distribution
mu_error, std_error = norm.fit(percent_error)

##Plot histogram
plt.figure()
plt.hist(percent_error, bins=16,
          density=True, alpha=0.6, color='g', label='Percent Error Data')
plt.plot(np.linspace(percent_error.min(), percent_error.max(), 100),
          norm.pdf(np.linspace(percent_error.min(), percent_error.max(), 100), 
                                loc=mu_error, scale=std_error), 'r-', label='Fitted Normal Distribution')
plt.xlabel('Percent Error')
plt.ylabel('Probability Density')
plt.title('Percent Error Distribution with Fitted Normal Curve')
plt.legend()

##Save and Show plot - Comment/Uncomment as necessary
plt.savefig('AMcP_ENGR315Exam2_percent_error_distribution.png')
##plt.show()