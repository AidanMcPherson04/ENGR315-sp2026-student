import numpy as np
from scipy.stats import ttest_1samp, norm, ttest_ind


def write_to_csv(filename: str, data):
    """
    Write an array of data to a file
    :param filename: Name of file to be written
    :param data: An array type object for data to be written to file
    :return: None
    """
    try:
        file = open(filename, 'w')
    except FileNotFoundError:
        print('Could not open file ', filename, ' error!!')
        return

    for a in data:
        file.writelines(str(a) + '\n')

    file.close()


def two_sided_tests(_files1: list, _files2: list , _alpha: float):
    """
    Conduct a two-sided t-test. Null hypothesis is they are equal.
    :param _files1: List of files to be tested. Assume they can be loaded directly as a numpy array
    :param _files2: List of files to be tested. Assume they can be loaded directly as a numpy array
    :param _alpha: Desired alpha value for t-test
    :return: A list of file pairs (tupple) where the null hypothesis is rejected
    """

    # list of files that are out of spec
    reject_null_hypothesis = []

    # YOUR CODE HERE #

    # return samples that were rejected
    return reject_null_hypothesis


if __name__ == "__main__":
    import matplotlib.pyplot as plot

    # number of samples for each distribution
    num_samples = 100

    # parameters for "gold standard" distribution
    target_mu = 0
    target_std = 1

    # take samples from the base distribution that will be our standard. Generate another that is very close
    equal_distribution_one = np.random.normal(loc=target_mu, scale=target_std, size=num_samples)
    equal_distribution_two = np.random.normal(loc=target_mu, scale=target_std, size=num_samples)

    # generate two distributions that should have mean that is less than
    less_than_distribution_one = np.random.normal(loc=target_mu - 0.5, scale=target_std, size=num_samples)
    less_than_distribution_two = np.random.normal(loc=target_mu - 1.0, scale=target_std, size=num_samples)

    # generate two distributions that should have mean that is greater than
    greater_than_distribution_one = np.random.normal(loc=target_mu + 0.5, scale=target_std, size=num_samples)
    greater_than_distribution_two = np.random.normal(loc=target_mu + 1.0, scale=target_std, size=num_samples)

    # write samples to files
    write_to_csv('equal1.txt', equal_distribution_one)
    write_to_csv('equal2.txt', equal_distribution_one)
    write_to_csv('lesser1.txt', less_than_distribution_one)
    write_to_csv('lesser2.txt', less_than_distribution_two)
    write_to_csv('greater1.txt', greater_than_distribution_one)
    write_to_csv('greater2.txt', greater_than_distribution_two)

    # Create file lists to compare
    first_test_files_1 = ['lesser1.txt', 'greater1.txt', 'equal1.txt']
    # perform two-sided tests for pairs (for same samples)
    not_equal_samples_1 = two_sided_tests(_files1=first_test_files_1, _files2=first_test_files_1, _alpha=0.5)
    print('Conducting two sided tests. All samples are not equal should be returned. Samples: ', not_equal_samples_1)

    # Create file lists to compare
    first_test_files_2 = ['lesser1.txt', 'lesser1.txt', 'greater1.txt', 'equal1.txt', 'equal1.txt']
    second_test_files_2 = ['lesser2.txt', 'lesser1.txt', 'greater2.txt', 'lesser1.txt', 'equal2.txt']
    # perform two-sided tests for pairs 
    not_equal_samples_2 = two_sided_tests(_files1=first_test_files_2, _files2=second_test_files_2, _alpha=0.5)
    print('Conducting two sided tests. All samples are not equal should be returned. Samples: ', not_equal_samples_2)

