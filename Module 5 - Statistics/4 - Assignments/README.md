**5.4.1 - One Sample Tests**

Complete the one-sample-tests function. It is provided a list of files that contain samples from a distribution. 
The function should return those file names where the sample rejects the NULL hypothesis during a one-sided t-test.
Note: your solution will need to open and load each file. It is suggested to use numpy to do this.

    def one_sample_tests(_files: list, _mean: float, _alpha: float, _less_than: bool):
        Conduct a one-sided t-test, either left or ride sided. Null hypothesis is the means are equal.
        :param _files: List of file names to be tested. Assume they can be loaded directly as a numpy array
        :param _mean: The test statistic mean for the hypothesis
        :param _alpha: Desired alpha value for t-test
        :param _less_than: If true, then a left-sided (<) t-test is performed. Otherwise, a right-sided test (>)
        :return: A list of files where the null hypothesis is rejected
