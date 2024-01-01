
import sys
import numpy as np
import scipy.stats
import plotly.graph_objects as go

true_mean = 6.0
true_std = 0.5
N = 10
alpha = 0.05
fig_filename_pattern = "figures/lectureEx_pdf_xbar.{:s}"

# simulate sample
sample = np.random.normal(loc=true_mean, scale=true_std, size=N)

# compute the standard error of the mean
se = true_std / np.sqrt(N)

# calculate the standard normal z value with alpha probability on the right
z_alpha = scipy.stats.norm.ppf(1-alpha)

# calculate the test critical value
critical_value = true_mean + se * z_alpha

# build plot
n_points = 100
x_dense = np.linspace(true_mean-3*se, true_mean+3*se, n_points)
pdf = scipy.stats.norm.pdf(x_dense, loc=true_mean, scale=se)

fig = go.Figure()
trace = go.Scatter(x=x_dense, y=pdf, mode="lines")
fig.add_trace(trace)
fig.add_vline(x=critical_value)
fig.update_layout(xaxis={"title": r"$\bar{x}$"}, yaxis={"title": "pdf"})

# save plot
fig.write_image(fig_filename_pattern.format("png"))
fig.write_html(fig_filename_pattern.format("html"))

# show plot
fig.show()
