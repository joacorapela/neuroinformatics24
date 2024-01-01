import math
import scipy.stats
import plotly.graph_objects as go

n = 35
x_bar_obs = 2.4
s = .29
alpha = 0.005
z_alpha = scipy.stats.norm.ppf(1-alpha)
mu_H0 = 2.3
ste_mean = s / math.sqrt(n)
print(f"ste_mean = {ste_mean}")
critical_value = mu_H0 + z_alpha * ste_mean
print(f"critical_value = {critical_value}")
p_value = 1 - scipy.stats.norm.cdf((x_bar_obs - mu_H0) / ste_mean)
print(f"p_value = {p_value}")


def compute_beta(mu_Ha, critical_value, ste_mean):
    beta = scipy.stats.norm.cdf((critical_value - mu_Ha) / ste_mean)
    return beta


mu_Has = [2.3, 2.4, 2.5, 2.6]
betas = [compute_beta(mu_Ha=mu_Ha,
                      critical_value=critical_value,
                      ste_mean=ste_mean) for mu_Ha in mu_Has]

fig = go.Figure()
trace = go.Scatter(x=mu_Has, y=betas, mode="lines+markers")
fig.add_trace(trace)
fig.update_layout(xaxis={"title": "mu_Ha"}, yaxis={"title": "beta"})
fig.show()

breakpoint()
