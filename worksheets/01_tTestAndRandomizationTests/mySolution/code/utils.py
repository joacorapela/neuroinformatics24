
import scipy.stats


def compute_beta(mu_Ha, critical_value, ste_mean):
    beta = scipy.stats.norm.cdf((critical_value - mu_Ha) / ste_mean)
    return beta
