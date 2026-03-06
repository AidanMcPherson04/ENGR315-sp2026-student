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


def one_sided_tests(_files: list, _mean: float, _alpha: float, _less_than: bool):
    """
    Conduct a one-sided t-test, either left or ride sided. Null hypothesis is the means are equal.
    :param _files: List of files to be tested. Assume they can be loaded directly as a numpy array
    :param _mean: The test statistic mean for the hypothesis
    :param _alpha: Desired alpha value for t-test
    :param _less_than: If true, then a left-sided (<) t-test is performed. Otherwise, a right-sided test (>)
    :return: A list of files where the null hypothesis is rejected
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
    base_distribution_one = np.random.normal(loc=target_mu, scale=target_std, size=num_samples)
    base_distribution_two = np.random.normal(loc=target_mu, scale=target_std, size=num_samples)

    # generate two distributions that should have mean that is less than
    less_than_distribution_one = np.random.normal(loc=target_mu - (0.5), scale=target_std, size=num_samples)
    less_than_distribution_two = np.random.normal(loc=target_mu - (1.0), scale=target_std, size=num_samples)

    # generate two distributions that should have mean that is greater than
    greater_than_distribution_one = np.random.normal(loc=target_mu + (0.5), scale=target_std, size=num_samples)
    greater_than_distribution_two = np.random.normal(loc=target_mu + (1.0), scale=target_std, size=num_samples)

    # write samples to files
    write_to_csv('base1.txt', base_distribution_one)
    write_to_csv('base2.txt', base_distribution_one)
    write_to_csv('lesser1.txt', less_than_distribution_one)
    write_to_csv('lesser2.txt', less_than_distribution_two)
    write_to_csv('greater1.txt', greater_than_distribution_one)
    write_to_csv('greater2.txt', greater_than_distribution_two)

    # place one-sided test files in a list
    one_sided_test_files = ['lesser1.txt', 'lesser2.txt', 'greater1.txt', 'greater2.txt']

    # perform all left-sided tests (rejected should be less than target as means not equal)
    left_sided_tests = one_sided_tests(_files=one_sided_test_files, _mean=target_mu, _alpha=0.5, _less_than=True)
    print('Conducting left sided tests. All samples less that mean should be returned. Samples: ', left_sided_tests)

    # perform all left-sided tests (rejected should be greater than target as means not equal)
    right_sided_tests = one_sided_tests(_files=one_sided_test_files, _mean=target_mu, _alpha=0.5, _less_than=False)
    print('Conducting right sided tests. All samples greater that mean should be returned. Samples: ', right_sided_tests)

