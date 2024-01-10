# From https://pages.stat.wisc.edu/~st571-1/d09.pdf

import math
import scipy.stats

mu_H0 = 3.35
s = 0.15
n = 100
mu_H1 = 3.4

alpha = 0.975
z_alpha = scipy.stats.norm.ppf(1-alpha)
ste = s / math.sqrt(n)
x_l = mu_H0 + z_alpha * ste
x_h = mu_H0 - z_alpha * ste
z_l = (x_l - mu_H1) / ste
z_h = (x_h - mu_H1) / ste
beta = scipy.stats.norm.cdf(z_h) - scipy.stats.norm.cdf(z_l)
power = 1 - beta
print(f"beta={beta}")
print(f"power={power}")

power = 0.8
beta = 1 - power
z_power = scipy.stats.norm.ppf(1-power)

breakpoint()
