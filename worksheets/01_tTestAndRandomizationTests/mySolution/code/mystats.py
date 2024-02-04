import math
import scipy.stats


def z_test(mu0, sample_mean, sample_std, n, alpha, test_type):
    z_obs = (sample_mean-mu0)/(sample_std/math.sqrt(n))

    if test_type == "two-sided":
        p_value = 2 * (1.0 - scipy.stats.norm.cdf(abs(z_obs)))
        z_critical = scipy.stats.norm.ppf(1-alpha/2)
    elif test_type == "right-sided":
        p_value = (1.0 - scipy.stats.norm.cdf(z_obs))
        z_critical = scipy.stats.norm.ppf(1-alpha)
    elif test_type == "left-sided":
        p_value = scipy.stats.norm.cdf(z_obs)
        z_critical = -scipy.stats.norm.ppf(1-alpha)

    return z_obs, z_critical, p_value


def t_test(mu0, sample_mean, sample_std, n, alpha, test_type):
    t_obs = (sample_mean-mu0)/(sample_std/math.sqrt(n))

    if test_type == "two-sided":
        p_value = 2 * (1.0 - scipy.stats.t.cdf(abs(t_obs), df=n-1))
        t_critical = scipy.stats.t.ppf(1-alpha/2, df=n-1)
    elif test_type == "right-sided":
        p_value = (1.0 - scipy.stats.t.cdf(t_obs, df=n-1))
        t_critical = scipy.stats.t.ppf(1-alpha, df=n-1)
    elif test_type == "left-sided":
        p_value = scipy.stats.t.cdf(t_obs, df=n-1)
        t_critical = -scipy.stats.t.ppf(1-alpha, df=n-1)

    return t_obs, t_critical, p_value


def compute_beta(mu_Ha, critical_value, ste_mean):
    beta = scipy.stats.norm.cdf((critical_value - mu_Ha) / ste_mean)
    return beta
