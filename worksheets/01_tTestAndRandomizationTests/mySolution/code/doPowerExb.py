
import sys
import math
import numpy as np
import scipy.stats
import plotly.graph_objects as go

import mystats


def main(argv):
    n = 16
    alpha = .05
    alpha2 = .01
    sigma = 16
    mu_H0 = 100

    ste_mean = sigma / math.sqrt(n)
    z_alpha = scipy.stats.norm.ppf(1-alpha)
    z_alpha2 = scipy.stats.norm.ppf(1-alpha2)
    critical_value = mu_H0 + ste_mean * z_alpha
    critical_value2 = mu_H0 + ste_mean * z_alpha2
    power = []
    power2 = []
    mu_Has = np.arange(mu_H0, mu_H0+20, 1)
    for mu_Ha in mu_Has:
        beta = mystats.compute_beta(mu_Ha, critical_value, ste_mean)
        power.append(1-beta)
        beta2 = mystats.compute_beta(mu_Ha, critical_value2, ste_mean)
        power2.append(1-beta2)

    fig = go.Figure()
    trace = go.Scatter(x=mu_Has, y=power, mode="lines+markers",
                       name=r"$\alpha={:.2f}$".format(alpha))
    fig.add_trace(trace)
    trace = go.Scatter(x=mu_Has, y=power2, mode="lines+markers",
                       name=r"$\alpha={:.2f}$".format(alpha2))
    fig.add_trace(trace)
    # fig.add_hline(y=alpha)
    fig.update_layout(xaxis=dict(title=r"$\mu$"), yaxis=dict(title="power"))

    fig_filename_pattern = "../figures/powerAtSignificanceLevels.{:s}"
    fig.write_image(fig_filename_pattern.format("png"))
    fig.write_html(fig_filename_pattern.format("html"))

    fig.show()


if __name__ == "__main__":
    main(sys.argv)
