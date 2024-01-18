
import math
import numpy as np
import scipy.stats
import plotly.graph_objects as go
# 
# N = 10
# alpha = 0.05
# fig_two_sided_filename_pattern = "figures/two_sided_pdf_z.{:s}"
# fig_one_sided_filename_pattern = "figures/one_sided_pdf_z.{:s}"
# 
# # calculate the standard normal z value with alpha probability on the right
# z_alpha = scipy.stats.norm.ppf(1-alpha)
# 
# # calculate the standard normal z value with alpha/2 probability on the right
# z_alphaOver2 = scipy.stats.norm.ppf(1-alpha/2)
# 
# # build plots
# n_points = 100
# x_dense = np.linspace(-3, +3, n_points)
# pdf = scipy.stats.norm.pdf(x_dense, loc=0, scale=1)
# 
# # one sided
# fig = go.Figure()
# trace = go.Scatter(x=x_dense, y=pdf, mode="lines")
# fig.add_trace(trace)
# fig.add_vline(x=-z_alphaOver2)
# fig.add_vline(x=z_alphaOver2)
# fig.update_layout(xaxis={"title": "z"}, yaxis={"title": "pdf"})
# fig.write_image(fig_two_sided_filename_pattern.format("png"))
# fig.write_html(fig_two_sided_filename_pattern.format("html"))
# fig.show()
# 
# # two sided
# fig = go.Figure()
# trace = go.Scatter(x=x_dense, y=pdf, mode="lines")
# fig.add_trace(trace)
# fig.add_vline(x=z_alpha)
# fig.update_layout(xaxis={"title": "z"}, yaxis={"title": "pdf"})
# fig.write_image(fig_one_sided_filename_pattern.format("png"))
# fig.write_html(fig_one_sided_filename_pattern.format("html"))
# fig.show()

# alpha and beta
mu_0 = 1.0
mu_a = 5.0
s = 10
n = 100
alpha = 0.01
n_x_dense = 100

z_alpha = scipy.stats.norm.ppf(1-alpha)
ste_mean = s / math.sqrt(n)
sample_mean_critical = mu_0 + ste_mean * z_alpha
x_min = mu_0 - 3 * ste_mean
x_max = mu_a + 3 * ste_mean
x_dense = np.linspace(x_min, x_max, n_x_dense)
pdf_0 = scipy.stats.norm.pdf(x_dense, loc=mu_0, scale=ste_mean)
pdf_a = scipy.stats.norm.pdf(x_dense, loc=mu_a, scale=ste_mean)

fig = go.Figure()
trace_0 = go.Scatter(x=x_dense, y=pdf_0,
                     name=r"$\text{dist} \bar{X} \text{under} H_0$")
fig.add_trace(trace_0)
trace_a = go.Scatter(x=x_dense, y=pdf_a,
                     name=r"$\text{dist} \bar{X} \text{under} H_a$")
fig.add_trace(trace_a)
fig.add_vline(x=sample_mean_critical)
fig.update_layout(xaxis={"title": r"$\bar{X}$"}, yaxis={"title": "pdf"})

fig_filename_pattern = "../figures/xBarUnderHaAndHa.{:s}"
fig.write_image(fig_filename_pattern.format("png"))
fig.write_html(fig_filename_pattern.format("html"))
fig.show()

breakpoint()
