import matplotlib.pyplot as plt
import numpy as np

# database name
database_name = 'mitdb_201'

# path to ekg folder
path_to_folder = "../../../data/ekg/"

# select a signal file to run
signal_filepath = path_to_folder + database_name + ".csv"

# load data in matrix from CSV file; skip first two rows
raw_ekg_data = np.loadtxt(signal_filepath, skiprows=2, delimiter=",")

time = raw_ekg_data[:, 0]
v5 = raw_ekg_data[:, 1]
v2 = raw_ekg_data[:, 2]

# pass data through LOW PASS FILTER (fs=250Hz, fc=15, N=6). These may not be correctly in radians
low_pass = np.convolve(v2,
                       [0.023834522, 0.093047634, 0.232148599, 0.301938491, 0.232148599, 0.093047634, 0.023834522])

# pass data through HIGH PASS FILTER (fs=250Hz, fc=5Hz, N=6) to create BAND PASS result
band_pass = np.convolve(low_pass,
                        [-0.000798178, -0.003095487, -0.007692586, 0.989209446, -0.007692586, -0.003095487,
                         -0.000798178])

# pass data through weighted differentiator
# I think this is incorrect as it does not look "forward" but should work
diff = np.convolve(band_pass, [1, 2, -2, -1])

# pass data through square function
squared = diff * diff

# pass through moving average of 150ms window @ 250 Hz => 38 samples
weights = np.ones(38)
signal = np.convolve(squared, weights)

# make a plot of the results. Can change the plot() parameter below to show different intermediate signals
plt.title('Process Signal for ' + database_name)
plt.plot(signal)
plt.show()