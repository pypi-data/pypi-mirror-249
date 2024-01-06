from math import sqrt

import numpy as np

from PEPit import PEP
from PEPit.functions import SmoothConvexFunction
from PEPit.primitive_steps import exact_linesearch_step


def wc_gradient_exact_line_search(L, gammas, wrapper="cvxpy", solver=None, verbose=1):
    """
    Consider the convex minimization problem

    .. math:: f_\\star \\triangleq \\min_x f(x),

    where :math:`f` is :math:`L`-smooth and :math:`\\mu`-strongly convex.

    This code computes a worst-case guarantee for the **gradient descent** (GD) with **exact linesearch** (ELS).
    That is, it computes the smallest possible :math:`\\tau(n, L, \\mu)` such that the guarantee

    .. math:: f(x_n) - f_\\star \\leqslant \\tau(n, L, \\mu) (f(x_0) - f_\\star)

    is valid, where :math:`x_n` is the output of the GD with ELS,
    and where :math:`x_\\star` is the minimizer of :math:`f`.
    In short, for given values of :math:`n`, :math:`L` and :math:`\\mu`,
    :math:`\\tau(n, L, \\mu)` is computed as the worst-case value of
    :math:`f(x_n)-f_\\star` when :math:`f(x_0) - f_\\star \\leqslant 1`.

    **Algorithm**:
    GD with ELS can be written as

        .. math:: x_{t+1} = x_t - \\gamma_t \\nabla f(x_t)

    with :math:`\\gamma_t = \\arg\\min_{\\gamma} f \\left( x_t - \\gamma \\nabla f(x_t) \\right)`.

    **Theoretical guarantee**: The **tight** worst-case guarantee for GD with ELS, obtained in [1, Theorem 1.2], is

        .. math:: f(x_n) - f_\\star \\leqslant \\left(\\frac{L-\\mu}{L+\\mu}\\right)^{2n} (f(x_0) - f_\\star).

    **References**: The detailed approach (based on convex relaxations) is available in [1], along with theoretical bound.

    `[1] E. De Klerk, F. Glineur, A. Taylor (2017). On the worst-case complexity of the gradient method with exact
    line search for smooth strongly convex functions. Optimization Letters, 11(7), 1185-1199.
    <https://link.springer.com/content/pdf/10.1007/s11590-016-1087-4.pdf>`_

    Args:
        L (float): the smoothness parameter.
        mu (float): the strong convexity parameter.
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
        >>> pepit_tau, theoretical_tau = wc_gradient_exact_line_search(L=1, mu=.1, n=2, wrapper="cvxpy", solver=None, verbose=1)
        [[ 0.0000e+00  3.8184e-01  6.1816e-01  1.4305e-05  1.4305e-05  1.4305e-05
           1.4305e-05  1.4305e-05  1.4305e-05  1.4305e-05  1.4365e-05  1.4365e-05
           1.4365e-05  9.8348e-06]
         [ 5.9605e-08  0.0000e+00  3.8184e-01  5.9605e-08  5.9605e-08  5.9605e-08
           5.9605e-08  5.9605e-08  5.9605e-08  5.9605e-08  5.9605e-08  5.9605e-08
           5.9605e-08  5.9605e-08]
         [ 5.9605e-08 -0.0000e+00  0.0000e+00  9.8682e-01  4.7760e-03  2.2259e-03
           1.4887e-03  1.1129e-03  8.7595e-04  7.1526e-04  6.0177e-04  5.1880e-04
           4.5204e-04  3.9482e-04]
         [ 5.9605e-08 -0.0000e+00  0.0000e+00  0.0000e+00  9.7168e-01  6.1913e-03
           2.6798e-03  1.6985e-03  1.2264e-03  9.5034e-04  7.7057e-04  6.4611e-04
           5.5170e-04  4.7946e-04]
         [ 5.9605e-08 -0.0000e+00  0.0000e+00  5.7220e-06  0.0000e+00  9.6094e-01
           6.7253e-03  2.8648e-03  1.7834e-03  1.2760e-03  9.8324e-04  7.9441e-04
           6.6376e-04  5.6839e-04]
         [ 5.9605e-08 -0.0000e+00  0.0000e+00  1.0252e-05  3.1590e-06  0.0000e+00
           9.5361e-01  7.1068e-03  2.9716e-03  1.8234e-03  1.2903e-03  9.8610e-04
           7.8821e-04  6.4564e-04]
         [ 5.9605e-08 -0.0000e+00  0.0000e+00  1.1086e-05  1.1504e-05  2.8610e-06
           0.0000e+00  9.4971e-01  7.2937e-03  2.9907e-03  1.8158e-03  1.2732e-03
           9.5797e-04  7.4387e-04]
         [ 5.9605e-08 -0.0000e+00  0.0000e+00  1.1623e-05  1.1742e-05  1.2457e-05
           2.3842e-06  0.0000e+00  9.4824e-01  7.2746e-03  2.9469e-03  1.7719e-03
           1.2217e-03  8.9502e-04]
         [ 5.9605e-08 -0.0000e+00  0.0000e+00  1.2696e-05  1.2279e-05  1.2636e-05
           1.2696e-05  1.9073e-06  0.0000e+00  9.4971e-01  7.0839e-03  2.8477e-03
           1.6804e-03  1.1358e-03]
         [ 5.9605e-08 -0.0000e+00  0.0000e+00  1.3769e-05  1.3173e-05  1.3173e-05
           1.2696e-05  1.2696e-05  1.6093e-06  0.0000e+00  9.5410e-01  6.7253e-03
           2.6608e-03  1.5440e-03]
         [ 5.9605e-08 -0.0000e+00  0.0000e+00  1.4842e-05  1.4246e-05  1.4246e-05
           1.3232e-05  1.2636e-05  1.2696e-05  2.2650e-06  0.0000e+00  9.6094e-01
           6.1531e-03  2.3918e-03]
         [ 5.9605e-08 -0.0000e+00  0.0000e+00  1.5140e-05  1.2875e-05  1.4722e-05
           1.4067e-05  1.2994e-05  1.2696e-05  1.2815e-05  3.9339e-06  0.0000e+00
           9.7070e-01  5.3673e-03]
         [ 5.9605e-08 -0.0000e+00  0.0000e+00  1.5259e-05  1.0371e-05  1.2994e-05
           1.4126e-05  1.3351e-05  1.2815e-05  1.2457e-05  1.2159e-05  7.0930e-06
           0.0000e+00  9.8584e-01]
         [ 5.9605e-08 -0.0000e+00  0.0000e+00  1.9550e-05  1.0192e-05  1.3113e-05
           1.4007e-05  1.3769e-05  1.3351e-05  1.0967e-05  1.1683e-05  1.0908e-05
           1.1265e-05  0.0000e+00]]
        [-998.2299471277933, -32.56109314889337, -31.580024483346524, -31.345429518202533, -31.19324808572798, -31.120407796422402, -31.123437577641756, -31.199323585604198, -31.34944804347524, -31.579299392593864, -31.89891530471088, -32.57139566788696]
        [3.81887385e-04 6.17960661e-03 1.42762901e-07 1.42933959e-07
         1.43049559e-07 1.43112619e-07 1.43191491e-07 1.43270747e-07
         1.43347286e-07 1.43430527e-07 1.43522454e-07 1.43585801e-07]
        ============= points ============================
        Point 0:
        [ 0.195 -0.981  0.     0.     0.     0.     0.     0.     0.     0.
          0.     0.     0.     0.     0.   ]
        [ 0.05386 -0.2712   0.2487   0.       0.       0.       0.       0.
          0.       0.       0.       0.       0.       0.       0.     ]
        Point 1:
        [ -53.66  270.2  -248.6     0.      0.      0.      0.      0.      0.
            0.      0.      0.      0.      0.      0.  ]
        [ 2.696e-02 -1.355e-01 -1.537e-01 -1.072e-04  0.000e+00  0.000e+00
          0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00
          0.000e+00  0.000e+00  0.000e+00]
        Point 2:
        [-5.634e+01  2.838e+02 -2.332e+02  1.072e-02  0.000e+00  0.000e+00
          0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00
          0.000e+00  0.000e+00  0.000e+00]
        [-3.827e-05  1.928e-04 -1.768e-04  2.158e-05  8.454e-04  0.000e+00
          0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00
          0.000e+00  0.000e+00  0.000e+00]
        Point 3:
        [-5.634e+01  2.838e+02 -2.332e+02  8.568e-03 -8.453e-02  0.000e+00
          0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00
          0.000e+00  0.000e+00  0.000e+00]
        [-3.827e-05  1.928e-04 -1.768e-04  1.252e-05 -8.297e-05 -8.416e-04
          0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00
          0.000e+00  0.000e+00  0.000e+00]
        Point 4:
        [-5.634e+01  2.838e+02 -2.332e+02  7.313e-03 -7.623e-02  8.417e-02
          0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00
          0.000e+00  0.000e+00  0.000e+00]
        [-3.827e-05  1.928e-04 -1.768e-04  7.153e-06 -8.279e-05  9.131e-05
         -8.364e-04  0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00
          0.000e+00  0.000e+00  0.000e+00]
        Point 5:
        [-5.634e+01  2.838e+02 -2.331e+02  6.599e-03 -6.793e-02  7.501e-02
          8.368e-02  0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00
          0.000e+00  0.000e+00  0.000e+00]
        [-3.827e-05  1.928e-04 -1.768e-04  5.364e-06 -8.273e-05  9.125e-05
          1.017e-04  8.302e-04  0.000e+00  0.000e+00  0.000e+00  0.000e+00
          0.000e+00  0.000e+00  0.000e+00]
        Point 6:
        [-5.634e+01  2.835e+02 -2.331e+02  6.062e-03 -5.969e-02  6.592e-02
          7.349e-02 -8.301e-02  0.000e+00  0.000e+00  0.000e+00  0.000e+00
          0.000e+00  0.000e+00  0.000e+00]
        [-3.8266e-05  1.9276e-04 -1.7679e-04  2.8610e-06 -8.2672e-05  9.1195e-05
          1.0163e-04 -1.1486e-04 -8.2254e-04  0.0000e+00  0.0000e+00  0.0000e+00
          0.0000e+00  0.0000e+00  0.0000e+00]
        Point 7:
        [-5.634e+01  2.835e+02 -2.331e+02  5.775e-03 -5.142e-02  5.676e-02
          6.329e-02 -7.153e-02  8.221e-02  0.000e+00  0.000e+00  0.000e+00
          0.000e+00  0.000e+00  0.000e+00]
        [-3.827e-05  1.928e-04 -1.767e-04  6.557e-07 -8.261e-05  9.114e-05
          1.016e-04 -1.148e-04  1.320e-04 -8.116e-04  0.000e+00  0.000e+00
          0.000e+00  0.000e+00  0.000e+00]
        Point 8:
        [-5.634e+01  2.835e+02 -2.331e+02  5.714e-03 -4.315e-02  4.767e-02
          5.316e-02 -6.006e-02  6.903e-02  8.118e-02  0.000e+00  0.000e+00
          0.000e+00  0.000e+00  0.000e+00]
        [-3.827e-05  1.928e-04 -1.767e-04 -1.013e-06 -8.261e-05  9.114e-05
          1.016e-04 -1.148e-04  1.320e-04  1.551e-04 -7.968e-04  0.000e+00
          0.000e+00  0.000e+00  0.000e+00]
        Point 9:
        [-5.631e+01  2.835e+02 -2.331e+02  5.814e-03 -3.488e-02  3.854e-02
          4.300e-02 -4.858e-02  5.585e-02  6.567e-02  7.971e-02  0.000e+00
          0.000e+00  0.000e+00  0.000e+00]
        [-3.8266e-05  1.9276e-04 -1.7667e-04 -2.9802e-06 -8.2552e-05  9.1076e-05
          1.0157e-04 -1.1474e-04  1.3185e-04  1.5509e-04  1.8811e-04 -7.7438e-04
          0.0000e+00  0.0000e+00  0.0000e+00]
        Point 10:
        [-5.631e+01  2.835e+02 -2.331e+02  6.115e-03 -2.664e-02  2.943e-02
          3.284e-02 -3.711e-02  4.266e-02  5.017e-02  6.088e-02  7.745e-02
          0.000e+00  0.000e+00  0.000e+00]
        [-3.8266e-05  1.9276e-04 -1.7667e-04 -5.5432e-06 -8.2493e-05  9.1076e-05
          1.0157e-04 -1.1474e-04  1.3185e-04  1.5497e-04  1.8811e-04  2.3925e-04
          7.3671e-04  0.0000e+00  0.0000e+00]
        Point 11:
        [-5.631e+01  2.835e+02 -2.331e+02  6.668e-03 -1.839e-02  2.032e-02
          2.269e-02 -2.563e-02  2.948e-02  3.467e-02  4.205e-02  5.350e-02
         -7.367e-02  0.000e+00  0.000e+00]
        [-3.827e-05  1.928e-04 -1.767e-04 -9.596e-06 -8.237e-05  9.096e-05
          1.015e-04 -1.147e-04  1.318e-04  1.550e-04  1.880e-04  2.393e-04
         -3.293e-04 -6.590e-04  0.000e+00]
        Point 12:
        [-5.6312e+01  2.8350e+02 -2.3300e+02  7.6256e-03 -1.0147e-02  1.1230e-02
          1.2535e-02 -1.4168e-02  1.6296e-02  1.9165e-02  2.3254e-02  2.9587e-02
         -4.0741e-02  6.5918e-02  0.0000e+00]
        [-3.8087e-05  1.9217e-04 -1.7631e-04  2.1994e-04 -8.7976e-05  9.4712e-05
          1.0419e-04 -1.1724e-04  1.3411e-04  1.5700e-04  1.9002e-04  2.4104e-04
         -3.3092e-04  5.3406e-04  7.2956e-04]
        ============= func vals ============================
        -0.0
        0.2073107674769132
        0.11684945511428176
        0.09549165542659993
        0.09549086853487405
        0.09549008295225625
        0.09548929821677098
        0.09548851417003455
        0.09548773025953118
        0.09548694619256962
        0.09548616158882074
        0.09548537592515084
        0.09548458874506476
        0.09548358051980087
        1.5092934008142933e-07<0.999999911524613
        ortho? -9.824906465830195e-05
        prod norms 0.00032936509237489585
        ================Bregmans================
        2.150431585579149e-08
        1.3045613912049392e-08
        
        
        
        
        
        ===========Gradients norms==================
        0.007849083024834646
        0.007849082913396643
        0.007849082840996334
        0.007849082824674761
        0.00784908281547394
        0.007849082819865164
        0.0078490828527398
        0.007849082896874433
        0.007849082934599452
        0.007849082938319166
        =========================================
        
        
        
        
        
        0.27641527146146694=0.27639320225002106
        0.13820627596630558=0.13819660112501053
        2.000019677318101
        [[ 5.3864e-02 -2.7124e-01  2.4866e-01  0.0000e+00  0.0000e+00  0.0000e+00
           0.0000e+00  0.0000e+00  0.0000e+00  0.0000e+00  0.0000e+00  0.0000e+00
           0.0000e+00  0.0000e+00  0.0000e+00]
         [ 2.6962e-02 -1.3550e-01 -1.5369e-01 -1.0723e-04  0.0000e+00  0.0000e+00
           0.0000e+00  0.0000e+00  0.0000e+00  0.0000e+00  0.0000e+00  0.0000e+00
           0.0000e+00  0.0000e+00  0.0000e+00]
         [-3.8266e-05  1.9276e-04 -1.7679e-04  2.1577e-05  8.4543e-04  0.0000e+00
           0.0000e+00  0.0000e+00  0.0000e+00  0.0000e+00  0.0000e+00  0.0000e+00
           0.0000e+00  0.0000e+00  0.0000e+00]
         [-3.8266e-05  1.9276e-04 -1.7679e-04  1.2517e-05 -8.2970e-05 -8.4162e-04
           0.0000e+00  0.0000e+00  0.0000e+00  0.0000e+00  0.0000e+00  0.0000e+00
           0.0000e+00  0.0000e+00  0.0000e+00]
         [-3.8266e-05  1.9276e-04 -1.7679e-04  7.1526e-06 -8.2791e-05  9.1314e-05
          -8.3637e-04  0.0000e+00  0.0000e+00  0.0000e+00  0.0000e+00  0.0000e+00
           0.0000e+00  0.0000e+00  0.0000e+00]
         [-3.8266e-05  1.9276e-04 -1.7679e-04  5.3644e-06 -8.2731e-05  9.1255e-05
           1.0169e-04  8.3017e-04  0.0000e+00  0.0000e+00  0.0000e+00  0.0000e+00
           0.0000e+00  0.0000e+00  0.0000e+00]
         [-3.8266e-05  1.9276e-04 -1.7679e-04  2.8610e-06 -8.2672e-05  9.1195e-05
           1.0163e-04 -1.1486e-04 -8.2254e-04  0.0000e+00  0.0000e+00  0.0000e+00
           0.0000e+00  0.0000e+00  0.0000e+00]
         [-3.8266e-05  1.9276e-04 -1.7667e-04  6.5565e-07 -8.2612e-05  9.1136e-05
           1.0163e-04 -1.1480e-04  1.3196e-04 -8.1158e-04  0.0000e+00  0.0000e+00
           0.0000e+00  0.0000e+00  0.0000e+00]
         [-3.8266e-05  1.9276e-04 -1.7667e-04 -1.0133e-06 -8.2612e-05  9.1136e-05
           1.0163e-04 -1.1480e-04  1.3196e-04  1.5509e-04 -7.9679e-04  0.0000e+00
           0.0000e+00  0.0000e+00  0.0000e+00]
         [-3.8266e-05  1.9276e-04 -1.7667e-04 -2.9802e-06 -8.2552e-05  9.1076e-05
           1.0157e-04 -1.1474e-04  1.3185e-04  1.5509e-04  1.8811e-04 -7.7438e-04
           0.0000e+00  0.0000e+00  0.0000e+00]
         [-3.8266e-05  1.9276e-04 -1.7667e-04 -5.5432e-06 -8.2493e-05  9.1076e-05
           1.0157e-04 -1.1474e-04  1.3185e-04  1.5497e-04  1.8811e-04  2.3925e-04
           7.3671e-04  0.0000e+00  0.0000e+00]
         [-3.8266e-05  1.9276e-04 -1.7667e-04 -9.5963e-06 -8.2374e-05  9.0957e-05
           1.0151e-04 -1.1468e-04  1.3185e-04  1.5497e-04  1.8799e-04  2.3925e-04
          -3.2926e-04 -6.5899e-04  0.0000e+00]
         [-3.8087e-05  1.9217e-04 -1.7631e-04  2.1994e-04 -8.7976e-05  9.4712e-05
           1.0419e-04 -1.1724e-04  1.3411e-04  1.5700e-04  1.9002e-04  2.4104e-04
          -3.3092e-04  5.3406e-04  7.2956e-04]]
        [[ 1.382e-01 -0.000e+00 -9.823e-05 -9.823e-05 -9.823e-05 -9.823e-05
          -9.823e-05 -9.823e-05 -9.823e-05 -9.823e-05 -9.823e-05 -9.823e-05
          -9.799e-05]
         [-0.000e+00  4.272e-02 -0.000e+00  0.000e+00  0.000e+00  0.000e+00
           0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00
           0.000e+00]
         [-9.823e-05 -0.000e+00  7.749e-07 -0.000e+00  0.000e+00  0.000e+00
           0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00
           0.000e+00]
         [-9.823e-05  0.000e+00 -0.000e+00  7.749e-07 -0.000e+00  0.000e+00
           0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00
           0.000e+00]
         [-9.823e-05  0.000e+00  0.000e+00 -0.000e+00  7.749e-07 -0.000e+00
           0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00
           0.000e+00]
         [-9.823e-05  0.000e+00  0.000e+00  0.000e+00 -0.000e+00  7.749e-07
          -0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00
           0.000e+00]
         [-9.823e-05  0.000e+00  0.000e+00  0.000e+00  0.000e+00 -0.000e+00
           7.749e-07 -0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00
           0.000e+00]
         [-9.823e-05  0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00
          -0.000e+00  7.749e-07 -0.000e+00  0.000e+00  0.000e+00  0.000e+00
           0.000e+00]
         [-9.823e-05  0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00
           0.000e+00 -0.000e+00  7.749e-07 -0.000e+00  0.000e+00  0.000e+00
           0.000e+00]
         [-9.823e-05  0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00
           0.000e+00  0.000e+00 -0.000e+00  7.749e-07 -0.000e+00  0.000e+00
           0.000e+00]
         [-9.823e-05  0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00
           0.000e+00  0.000e+00  0.000e+00 -0.000e+00  7.749e-07 -0.000e+00
           0.000e+00]
         [-9.823e-05  0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00
           0.000e+00  0.000e+00  0.000e+00  0.000e+00 -0.000e+00  7.749e-07
          -0.000e+00]
         [-9.799e-05  0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00
           0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00 -0.000e+00
           1.252e-06]]
        [[ 1.000e+00 -0.000e+00 -2.983e-01 -2.983e-01 -2.983e-01 -2.983e-01
          -2.983e-01 -2.983e-01 -2.983e-01 -2.983e-01 -2.983e-01 -2.983e-01
          -2.383e-01]
         [-0.000e+00  1.000e+00 -1.192e-07  0.000e+00  0.000e+00  0.000e+00
           0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00  0.000e+00
           0.000e+00]
         [-2.983e-01 -1.192e-07  1.000e+00 -2.587e-05  1.371e-06  1.192e-06
           1.192e-06  1.192e-06  1.192e-06  1.192e-06  1.132e-06  1.132e-06
           4.172e-07]
         [-2.983e-01  0.000e+00 -2.587e-05  1.000e+00 -2.629e-05  1.311e-06
           1.252e-06  1.252e-06  1.252e-06  1.192e-06  1.192e-06  1.132e-06
           4.768e-07]
         [-2.983e-01  0.000e+00  1.371e-06 -2.629e-05  1.000e+00 -2.664e-05
           1.490e-06  1.371e-06  1.311e-06  1.311e-06  1.252e-06  1.192e-06
           5.364e-07]
         [-2.983e-01  0.000e+00  1.192e-06  1.311e-06 -2.664e-05  1.000e+00
          -2.694e-05  1.729e-06  1.490e-06  1.431e-06  1.371e-06  1.311e-06
           5.960e-07]
         [-2.983e-01  0.000e+00  1.192e-06  1.252e-06  1.490e-06 -2.694e-05
           1.000e+00 -2.700e-05  1.907e-06  1.609e-06  1.490e-06  1.371e-06
           6.557e-07]
         [-2.983e-01  0.000e+00  1.192e-06  1.252e-06  1.371e-06  1.729e-06
          -2.700e-05  1.000e+00 -2.682e-05  1.967e-06  1.609e-06  1.490e-06
           7.153e-07]
         [-2.983e-01  0.000e+00  1.192e-06  1.252e-06  1.311e-06  1.490e-06
           1.907e-06 -2.682e-05  1.000e+00 -2.640e-05  1.907e-06  1.609e-06
           7.749e-07]
         [-2.983e-01  0.000e+00  1.192e-06  1.192e-06  1.311e-06  1.431e-06
           1.609e-06  1.967e-06 -2.640e-05  1.000e+00 -2.593e-05  1.848e-06
           8.941e-07]
         [-2.983e-01  0.000e+00  1.132e-06  1.192e-06  1.252e-06  1.371e-06
           1.490e-06  1.609e-06  1.907e-06 -2.593e-05  1.000e+00 -2.539e-05
           1.013e-06]
         [-2.983e-01  0.000e+00  1.132e-06  1.132e-06  1.192e-06  1.311e-06
           1.371e-06  1.490e-06  1.609e-06  1.848e-06 -2.539e-05  1.000e+00
          -2.009e-05]
         [-2.383e-01  0.000e+00  4.172e-07  4.768e-07  5.364e-07  5.960e-07
           6.557e-07  7.153e-07  7.749e-07  8.941e-07  1.013e-06 -2.009e-05
           1.000e+00]]
        Taux = 0.09548357268573207
        0.09549150281252627
        0.09548806762897645
        -1.7642329086401318
    
    """

    # Instantiate PEP
    problem = PEP()

    # Declare a smooth strongly convex function
    func = problem.declare_function(SmoothConvexFunction, L=L)

    # Start by defining its unique optimal point xs = x_* and corresponding function value fs = f_*
    xs = func.stationary_point()
    fs = func(xs)
    problem.add_constraint(fs == 0)

    # Then define the starting point x0 of the algorithm as well as corresponding gradient and function value g0 and f0
    x0 = problem.set_initial_point()
    g0, f0 = func.oracle(x0)

    # Set the initial constraint that is the difference between f0 and f_*
    problem.set_initial_condition((x0 - xs) ** 2 <= 1)
    # problem.set_initial_condition(f0-fs <= 1)

    # Run n steps of GD method with ELS
    x = x0
    gx = g0
    all_gradients = [g0]
    for gamma in gammas:
        x = x - gamma * gx
        g_prev = gx
        gx, fx = func.oracle(x)
        func.add_constraint(gx * g_prev == 0)
        all_gradients.append(gx)

    for i in range(1, len(gammas) + 1):
        for l in range(1, len(gammas) + 1):
            if l != i:
                problem.add_constraint(all_gradients[i] * all_gradients[l] == 0)

    for i in range(2, len(gammas)):
        for j in range(2, len(gammas)):
            if i != j:
                problem.add_constraint(all_gradients[i] ** 2 == all_gradients[j] ** 2)

    # for pointi in func.list_of_points:
    #     for pointj in func.list_of_points:
    #         if pointi != pointj:
    #             func.add_constraint(pointi[1] * pointj[1] == 0)

    # Set the performance metric to the function value accuracy
    problem.set_performance_metric(fx - fs)
    # problem.set_performance_metric(gx ** 2)

    # Solve the PEP
    pepit_verbose = max(verbose, 0)
    pepit_tau = problem.solve(wrapper=wrapper, solver=solver, verbose=pepit_verbose)

    n = len(gammas)
    ic_duals = [constraint.eval_dual() for constraint in func.list_of_class_constraints]
    ic_duals_squared = [0]
    for i in range(n + 1):
        ic_duals_squared += ic_duals[i * (n + 2): (i + 1) * (n + 2)]
        ic_duals_squared += [0]
    ic_duals_squared = np.array(ic_duals_squared).reshape((n + 2, n + 2))
    ortho_dual = [constraint.eval_dual() for constraint in func.list_of_constraints]
    print(ic_duals_squared.astype(np.float16))
    print(ortho_dual)
    print(ic_duals_squared[0, 1:-1] / np.array(gammas))
    # eta_est = (sqrt((gamma-1)*(gamma+3)) - (gamma-1))/2
    # rho_est = (gamma*sqrt((gamma-1)*(gamma+3)) - (gamma-1)*(gamma+2))/4
    # xi_est = (1-eta_est)**2 / (4*rho_est) - 1/2
    # eta = ic_duals[0]
    # rho = pepit_tau
    # xi = ic_duals[5]
    # ortho_dual_est = gamma/4 * (-5*(L*gamma+3)*(L*gamma-1) + (7*L*gamma-3)*sqrt((L*gamma+3)*(L*gamma-1))) / ((L*gamma-1)*(7-3*L*gamma))
    # print("{}={}".format(eta_est, eta))
    # print("{}={}".format(rho_est, rho))
    # print("{}={}".format(xi_est, xi))
    # print("{}={}".format(ortho_dual_est, ortho_dual[0]))
    points = []
    grads = []
    vals = []
    for point in func.list_of_points:
        points.append((point[0] - xs).eval())
        grads.append(point[1].eval())
        vals.append(point[2].eval())

    print("============= points ============================")
    for i, point, grad in zip(range(n + 1), points[1:], grads[1:]):
        print("Point {}:".format(i))
        print(point.astype(np.float16))
        print(grad.astype(np.float16))

    # print("============= grads ============================")
    # for grad in grads:
    print("============= func vals ============================")
    for val in vals:
        print(val)

    eta = (3 - sqrt(5)) / 2
    rho = pepit_tau
    g1 = func.list_of_points[2][1]
    res_vec = x0 - xs - (eta * g0 + (1 - eta) * g1) / (2 * rho)
    res = res_vec ** 2
    print("{}<{}".format(res.eval(), ((x0 - xs) ** 2).eval()))
    print("ortho? {}".format((func.list_of_points[3][1] * g0).eval()))
    print("prod norms {}".format((sqrt((func.list_of_points[3][1] ** 2).eval() * (g0 ** 2).eval()))))
    # print(func.list_of_points[3][1].eval().astype(np.float16))
    # print(g0.eval())
    # print(g0.eval() / func.list_of_points[3][1].eval().astype(np.float16))

    print("================Bregmans================")
    print(- vals[1] + np.dot(grads[1], points[1]) - 1 / 2 * np.dot(grads[1], grads[1]))
    print(- vals[2] + np.dot(grads[2], points[2]) - 1 / 2 * np.dot(grads[2], grads[2]))
    # print(- vals[3] + np.dot(grads[3], points[3]) - 1/2 * np.dot(grads[3], grads[3]))
    # print(vals[3] - np.dot(grads[3], points[3]), 1/2 * np.dot(grads[3], grads[3]))

    print("\n\n\n\n\n===========Gradients norms==================")

    for i in range(2, len(gammas)):
        print(gammas[i] ** 2 * np.dot(grads[i + 1], grads[i + 1]))

    print("=========================================\n\n\n\n\n")

    print("{}={}".format((g0 * (x0 - xs)).eval(), (1 - 1 / sqrt(5)) / 2))
    print("{}={}".format((g1 * (x0 - xs)).eval(), (1 - 1 / sqrt(5)) / 4))
    print((g0 * (x0 - xs)).eval() / (g1 * (x0 - xs)).eval())

    grads_transposed = np.array(grads)[1:, :]
    print(grads_transposed.astype(np.float16))
    # grads_transposed = grads_transposed[2:, :]
    print((grads_transposed @ grads_transposed.T).astype(np.float16))
    normed_grads_transposed = grads_transposed / np.sqrt(np.sum(grads_transposed ** 2, axis=1)).reshape(-1, 1)
    print((normed_grads_transposed @ normed_grads_transposed.T).astype(np.float16))

    def is_colinear(i, j):
        print("colinear? {}".format((func.list_of_points[i + 1][1] * func.list_of_points[j + 1][1]).eval() / (
            sqrt((func.list_of_points[i + 1][1] ** 2).eval() * (func.list_of_points[j + 1][1] ** 2).eval()))))

    # is_colinear(0, 2)
    # is_colinear(1, 3)
    # is_colinear(2, 4)
    # is_colinear(3, 5)

    # Compute theoretical guarantee (for comparison)
    theoretical_tau = 1 / len(gammas)

    # Print conclusion if required
    if verbose != -1:
        print('*** Example file: worst-case performance of gradient descent with exact linesearch (ELS) ***')
        print('\tPEPit guarantee:\t\t f(x_n)-f_* <= {:.6} (f(x_0)-f_*)'.format(pepit_tau))
        print('\tTheoretical guarantee:\t f(x_n)-f_* <= {:.6} (f(x_0)-f_*)'.format(theoretical_tau))

    # Return the worst-case guarantee of the evaluated method (and the reference theoretical value)
    return pepit_tau, theoretical_tau


if __name__ == "__main__":
    gamma = 100
    pepit_tau, _ = wc_gradient_exact_line_search(L=1, gammas=[1000] + [gamma] * 11, verbose=-1)
    print("Taux = {}".format(pepit_tau))
    print(1 / 8 * (3 - sqrt(5)))
    print(1 / 8 * (3 - sqrt(5)) - (5 - 2 * sqrt(5)) / 16 / (gamma - 2) ** 2)

    upperbound = 1 / 8 * (3 - sqrt(5))
    lowerbound = 1 / 8 * (3 - sqrt(5)) - (5 - 2 * sqrt(5)) / 16 / (gamma - 2) ** 2
    print((upperbound - pepit_tau) / (pepit_tau - lowerbound))
