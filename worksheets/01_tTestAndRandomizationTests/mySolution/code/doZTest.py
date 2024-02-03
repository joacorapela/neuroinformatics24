import sys
import warnings
import argparse
import math
import numpy as np
import scipy.stats
import mystats

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--xbar", type=float, help="sample mean", default=None)
    parser.add_argument("--s", type=float, help="sample standard deviation",
                        default=None)
    parser.add_argument("--n", type=int, help="sample size", default=None)
    parser.add_argument("--data_filename", type=str,
                        help="data filename (csv format)",
                        default=None)
    parser.add_argument("mu0", type=float, help="null hypothesis mean")
    parser.add_argument("alpha", type=float, help="confidence level")
    parser.add_argument("test_type", type=str,
                        help="test type (left-sided, right-sided, two-sided)")
    args = parser.parse_args()

    xbar = args.xbar
    mu0 = args.mu0
    s = args.s
    n = args.n
    alpha = args.alpha
    test_type = args.test_type
    data_filename = args.data_filename

    if data_filename is not None:
        data = np.genfromtxt(data_filename, delimiter=",")
        if xbar is not None:
            warnings.warn("Overriding the provided sample mean with that "
                          "calculated from the data")
        xbar = np.mean(data)
        if s is not None:
            warnings.warn("Overriding the provided sample std with that "
                          "calculated from the data")
        s = np.std(data)
        if n is not None:
            warnings.warn("Overriding the provided sample sample size with that "
                          "calculated from the data")
        n = len(data)

    z_obs, z_critical, p_value = mystats.z_test(mu0=mu0, sample_mean=xbar,
                                                sample_std=s, n=n, alpha=alpha,
                                                test_type=test_type)
    print(f"z_obs = {z_obs}")
    print(f"z_critical = {z_critical}")
    print(f"p_value = {p_value}")

    breakpoint()


if __name__ == "__main__":
    main(sys.argv)
