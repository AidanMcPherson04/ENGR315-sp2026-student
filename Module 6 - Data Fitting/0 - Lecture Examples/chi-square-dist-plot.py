from scipy.stats import chisquare, chi2
import matplotlib.pyplot as plt
import numpy as np

"""
Generate several chi2 plots based upon DoF
"""
DoF = [3, 4, 5, 7, 10]

# create x-axis for chi2 plot
for df in DoF:
    x = np.linspace(chi2.ppf(0.01, df), chi2.ppf(0.99, df), 1000)
    plt.plot(x, chi2.pdf(x, df),label='DoF='+str(df))

plt.title('Chi2 Distribution for Various Degrees of Freedom')
plt.xlabel('Chi2 Stat')
plt.legend()
plt.show()

