
import sys
import numpy as np
import scipy.stats
import plotly.graph_objects as go

N = 10
alpha = 0.05
fig_two_sided_filename_pattern = "figures/two_sided_pdf_z.{:s}"
fig_one_sided_filename_pattern = "figures/one_sided_pdf_z.{:s}"

# calculate the standard normal z value with alpha probability on the right
z_alpha = scipy.stats.norm.ppf(1-alpha)

# calculate the standard normal z value with alpha/2 probability on the right
z_alphaOver2 = scipy.stats.norm.ppf(1-alpha/2)

# build plots
n_points = 100
x_dense = np.linspace(-3, +3, n_points)
pdf = scipy.stats.norm.pdf(x_dense, loc=0, scale=1)

# one sided
fig = go.Figure()
trace = go.Scatter(x=x_dense, y=pdf, mode="lines")
fig.add_trace(trace)
fig.add_vline(x=-z_alphaOver2)
fig.add_vline(x=z_alphaOver2)
fig.update_layout(xaxis={"title": "z"}, yaxis={"title": "pdf"})
fig.write_image(fig_two_sided_filename_pattern.format("png"))
fig.write_html(fig_two_sided_filename_pattern.format("html"))
fig.show()

# two sided
fig = go.Figure()
trace = go.Scatter(x=x_dense, y=pdf, mode="lines")
fig.add_trace(trace)
fig.add_vline(x=z_alpha)
fig.update_layout(xaxis={"title": "z"}, yaxis={"title": "pdf"})
fig.write_image(fig_one_sided_filename_pattern.format("png"))
fig.write_html(fig_one_sided_filename_pattern.format("html"))
fig.show()

breakpoint()
