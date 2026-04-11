**5.4.1 - One Sided for One Sample Tests**

Complete the one-sided-tests function for One Sample. It is provided a list of files that contain samples from a distribution. 
The function should return those file names where the sample rejects the NULL hypothesis during a one-sided t-test.
Note: your solution will need to open and load each file. It is suggested to use numpy to do this.

    def one-sided-tests(_files: list, _mean: float, _alpha: float, _less_than: bool):
        Conduct a one-sided t-test, either left or ride sided. Null hypothesis is the means are equal.
        :param _files: List of file names to be tested. Assume they can be loaded directly as a numpy array
        :param _mean: The test statistic mean for the hypothesis
        :param _alpha: Desired alpha value for t-test
        :param _less_than: If true, then a left-sided (<) t-test is performed. Otherwise, a right-sided test (>)
        :return: A list of files where the null hypothesis is rejected

**5.4.2 - Two Sided for Two Samples Tests**

Complete the two-sided-tests function for Two Samples. It is provided a list of files that contain samples from a distribution. 
The function should return those file names where the sample rejects the NULL hypothesis during a two-sided t-test.
Note: your solution will need to open and load each file. It is suggested to use numpy to do this.

    def two_sided_tests(_files1: list, _files2: list , _alpha: float):
        """
        Conduct a two-sided t-test. Null hypothesis is they are equal.
        :param _files1: List of files to be tested. Assume they can be loaded directly as a numpy array
        :param _files2: List of files to be tested. Assume they can be loaded directly as a numpy array
        :param _alpha: Desired alpha value for t-test
        :return: A list of file pairs (tupple) where the null hypothesis is rejected
        """