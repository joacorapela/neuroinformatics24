
import sys
import math
import numpy as np
import scipy.stats
import plotly.graph_objects as go

import mystats


def main(argv):
    n = 16
    sigma = 16
    alpha = 0.05
    beta = 0.2
    mu_H0 = 100
    mu_Ha = 112

    z_alpha = scipy.stats.norm.ppf(1-alpha)
    z_beta = scipy.stats.norm.ppf(1-beta)
    n = math.ceil((sigma / (mu_Ha - mu_H0) * (z_alpha + z_beta))**2)

    print(f"minimum n={n}")

    ste_mean = sigma / math.sqrt(n)
    critical_value = mu_H0 + ste_mean * z_alpha
    mu_Has = np.arange(mu_H0, mu_H0+20, 1)
    power = []
    for a_mu_Ha in mu_Has:
        beta = mystats.compute_beta(a_mu_Ha, critical_value, ste_mean)
        power.append(1-beta)

    fig = go.Figure()
    trace = go.Scatter(x=mu_Has, y=power, mode="lines+markers")
    fig.add_trace(trace)
    fig.update_layout(xaxis=dict(title=r"$\mu$"), yaxis=dict(title="power"))

    fig_filename_pattern = "../figures/powerForMinN_muHa{:.02f}.{:s}"
    fig.write_image(fig_filename_pattern.format(mu_Ha, "png"))
    fig.write_html(fig_filename_pattern.format(mu_Ha, "html"))

    fig.show()


if __name__ == "__main__":
    main(sys.argv)
