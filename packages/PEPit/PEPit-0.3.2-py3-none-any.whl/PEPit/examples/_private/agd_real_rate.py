from math import sqrt
import numpy as np

from PEPit import PEP
from PEPit.functions import SmoothStronglyConvexFunction


def wc_accelerated_gradient_strongly_convex(mu, L, n, wrapper="cvxpy", solver=None, verbose=1):
    """
    Consider the convex minimization problem

    .. math:: f_\\star \\triangleq \\min_x f(x),

    where :math:`f` is :math:`L`-smooth and :math:`\\mu`-strongly convex.

    This code computes a worst-case guarantee for an **accelerated gradient** method, a.k.a **fast gradient** method.
    That is, it computes the smallest possible :math:`\\tau(n, L, \\mu)` such that the guarantee

    .. math:: f(x_n) - f_\\star \\leqslant \\tau(n, L, \\mu) \\left(f(x_0) -  f(x_\\star) + \\frac{\\mu}{2}\\|x_0 - x_\\star\\|^2\\right),

    is valid, where :math:`x_n` is the output of the **accelerated gradient** method,
    and where :math:`x_\\star` is the minimizer of :math:`f`.
    In short, for given values of :math:`n`, :math:`L` and :math:`\\mu`,
    :math:`\\tau(n, L, \\mu)` is computed as the worst-case value of
    :math:`f(x_n)-f_\\star` when :math:`f(x_0) -  f(x_\\star) + \\frac{\\mu}{2}\\|x_0 - x_\\star\\|^2 \\leqslant 1`.

    **Algorithm**:
    For :math:`t \\in \\{0, \\dots, n-1\\}`,

        .. math::
            :nowrap:

            \\begin{eqnarray}
                y_t & = & x_t + \\frac{\\sqrt{L} - \\sqrt{\\mu}}{\\sqrt{L} + \\sqrt{\\mu}}(x_t - x_{t-1}) \\\\
                x_{t+1} & = & y_t - \\frac{1}{L} \\nabla f(y_t)
            \\end{eqnarray}

    with :math:`x_{-1}:= x_0`.

    **Theoretical guarantee**:

        The following **upper** guarantee can be found in [1,  Corollary 4.15]:

        .. math:: f(x_n)-f_\\star \\leqslant \\left(1 - \\sqrt{\\frac{\\mu}{L}}\\right)^n \\left(f(x_0) -  f(x_\\star) + \\frac{\\mu}{2}\\|x_0 - x_\\star\\|^2\\right).

    **References**:

    `[1] A. d’Aspremont, D. Scieur, A. Taylor (2021). Acceleration Methods. Foundations and Trends
    in Optimization: Vol. 5, No. 1-2.
    <https://arxiv.org/pdf/2101.09545.pdf>`_

    Args:
        mu (float): the strong convexity parameter
        L (float): the smoothness parameter.
        n (int): number of iterations.
        wrapper (str): the name of the wrapper to be used.
        solver (str): the name of the solver the wrapper should use.
		verbose (int): level of information details to print.

                        - -1: No verbose at all.
                        - 0: This example's output.
                        - 1: This example's output + PEPit information.
                        - 2: This example's output + PEPit information + solver details.

    Returns:
        pepit_tau (float): worst-case value
        theoretical_tau (float): theoretical value

    Example:
        >>> pepit_tau, theoretical_tau = wc_accelerated_gradient_strongly_convex(mu=0.1, L=1, n=2, wrapper="cvxpy", solver=None, verbose=1)
    
    """

    # Instantiate PEP
    problem = PEP()

    # Declare a strongly convex smooth function
    func = problem.declare_function(SmoothStronglyConvexFunction, mu=mu, L=L)

    # Start by defining its unique optimal point xs = x_* and corresponding function value fs = f_*
    xs = func.stationary_point()
    fs = func(xs)

    # Then define the starting point x0 of the algorithm
    x0 = problem.set_initial_point()

    # Set the initial constraint that is a well-chosen distance between x0 and x^*
    problem.set_initial_condition((x0 - xs) ** 2 <= 1)

    # Run n steps of the fast gradient method
    kappa = mu / L
    x_new = x0
    y = x0
    for i in range(n):
        x_old = x_new
        x_new = y - 1 / L * func.gradient(y)
        y = x_new + (1 - sqrt(kappa)) / (1 + sqrt(kappa)) * (x_new - x_old)

    # Set the performance metric to the function value accuracy
    problem.set_performance_metric((y - xs) ** 2)

    # Solve the PEP
    pepit_verbose = max(verbose, 0)
    pepit_tau = problem.solve(wrapper=wrapper, solver=solver, verbose=pepit_verbose)

    # Compute theoretical guarantee (for comparison)
    b = 2 * (3 - sqrt(kappa))
    c = -15 + 10 * sqrt(kappa) + kappa
    d = 8 * (1 - sqrt(kappa))
    delta0 = b ** 2 - 3 * c
    delta1 = 2 * b ** 3 - 9 * b * c + 27 * d
    root2 = delta1 ** 2 - 4 * delta0 ** 3
    if root2 >= 0:
        root = sqrt(root2)
    else:
        root = sqrt(-root2) * 1j
    C1 = ((delta1 + root) / 2) ** (1 / 3)
    X1 = -(C1 + delta0 / C1 + b) / 3
    x1 = X1.real
    C2 = C1 * (-1 / 2 + 1j * sqrt(3) / 2)
    X2 = -(C2 + delta0 / C2 + b) / 3
    x2 = X2.real
    C3 = C2 * (-1 / 2 + 1j * sqrt(3) / 2)
    X3 = -(C3 + delta0 / C3 + b) / 3
    x3 = X3.real
    x = np.array([x1, x2, x3])
    x = x[0 <= x]
    theoretical_tau = ((1 - sqrt(kappa)) * np.min(x)) ** n

    former_theoretical_tau = (1 - sqrt(kappa)) ** n
    if mu == 0:
        print("Warning: momentum is tuned for strongly convex functions!")

    # Print conclusion if required
    if verbose != -1:
        print('*** Example file: worst-case performance of the accelerated gradient method ***')
        print('\tPEPit guarantee:\t\t f(x_n)-f_* <= {:.6} (f(x_0) - f(x_*))'.format(
            pepit_tau))
        print('\tTheoretical guarantee:\t f(x_n)-f_* <= {:.6} (f(x_0) - f(x_*))'.format(
            theoretical_tau))

    # Return the worst-case guarantee of the evaluated method (and the reference theoretical value)
    return pepit_tau, former_theoretical_tau, theoretical_tau


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    pepit_taus = []
    former_theoretical_taus = []
    theoretical_taus = []
    for n in range(2, 20):
        pepit_tau, former_theoretical_tau, theoretical_tau = wc_accelerated_gradient_strongly_convex(mu=0.1, L=1, n=n,
                                                                                                     verbose=-1)
        pepit_taus.append(pepit_tau)
        former_theoretical_taus.append(former_theoretical_tau)
        theoretical_taus.append(theoretical_tau)

    plt.plot(pepit_taus)
    plt.plot(former_theoretical_taus)
    plt.plot(theoretical_taus)
    plt.yscale("log")
    plt.show()
