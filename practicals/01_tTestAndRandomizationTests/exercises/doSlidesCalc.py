
import math
import scipy.stats

alpha = 0.01
z_alpha = scipy.stats.norm.ppf(1-alpha)
mu_0 = 1.0
mu_a = 5.0
s = 10.0
n = 100
z_upper = (mu_0 - mu_a) / (s/math.sqrt(n)) + z_alpha
beta = scipy.stats.norm.cdf(z_upper)

breakpoint()
