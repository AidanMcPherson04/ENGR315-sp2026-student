import math


def my_pi(target_error):
    """
    Implementation of Gauss–Legendre algorithm to approximate PI from https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm

    :param target_error: Desired error for PI estimation
    :return: Approximation of PI to specified error bound
    """

    ### YOUR CODE HERE ###
    a = 1
    b = 1 / math.sqrt(2)
    t = 1 / 4
    p = 1
    
    for i in range(1, 10):
        a_n = (a + b) / 2
        b_n = math.sqrt(a * b)
        t_n = t - p * (a_n - a) ** 2
        p_n = 2 * p
        a = a_n
        b = b_n
        p = p_n
        t = t_n
        p = p_n

    targeterror = ((a + b) ** 2) / (4 * t)
    # change this so an actual value is returned
    return targeterror




desired_error = 1E-10

approximation = my_pi(desired_error)

print("Solution returned PI=", approximation)

error = abs(math.pi - approximation)
print("Error is", error)
if error < abs(desired_error):
    print("Solution is acceptable")
else:
    print("Solution is not acceptable")
