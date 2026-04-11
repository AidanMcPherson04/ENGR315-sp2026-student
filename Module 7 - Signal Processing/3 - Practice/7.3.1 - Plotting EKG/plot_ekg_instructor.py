import matplotlib.pyplot as plt
import numpy as np

# import the CSV file using numpy
path = '../../../data/ekg/mitdb_201.csv'

# load data in matrix from CSV file; skip first two rows

# load data in matrix from CSV file; skip first two rows
ekg_data = np.loadtxt(path, skiprows=2, delimiter=",")

# save each vector as own variable
time = ekg_data[:, 0]
v5 = ekg_data[:, 1]
v2 = ekg_data[:, 2]

# use matplot lib to generate a single graph

plt.xlabel('Time (s)')
plt.ylabel('Signal (mV)')
plt.title('EKG Signal')
plt.plot(time, v2)
plt.show()
