
import sys
import math
import numpy as np
import scipy.stats
import plotly.graph_objects as go

import mystats


def main(argv):
    n = 16
    alpha = .05
    sigma = 16
    mu_H0 = 100

    z_alpha = scipy.stats.norm.ppf(1-alpha)
    ste_mean = sigma / math.sqrt(n)
    critical_value = mu_H0 + ste_mean * z_alpha

    mu_Ha = 108
    beta = mystats.compute_beta(mu_Ha, critical_value, ste_mean)
    print(f"mu_Ha={mu_Ha}: power={1-beta}")

    mu_Ha = 112
    beta = mystats.compute_beta(mu_Ha, critical_value, ste_mean)
    print(f"mu_Ha={mu_Ha}: power={1-beta}")

    mu_Ha = 116
    beta = mystats.compute_beta(mu_Ha, critical_value, ste_mean)
    print(f"mu_Ha={mu_Ha}: power={1-beta}")

    mu_Has = np.arange(mu_H0, mu_H0+20, 1)
    power = []
    for mu_Ha in mu_Has:
        beta = mystats.compute_beta(mu_Ha, critical_value, ste_mean)
        power.append(1-beta)

    fig = go.Figure()
    trace = go.Scatter(x=mu_Has, y=power, mode="lines+markers")
    fig.add_trace(trace)
    # fig.add_hline(y=alpha)
    fig.update_layout(xaxis=dict(title=r"$\mu$"), yaxis=dict(title="power"))

    fig_filename_pattern = "../figures/powerVsEffectSize.{:s}"
    fig.write_image(fig_filename_pattern.format("png"))
    fig.write_html(fig_filename_pattern.format("html"))

    fig.show()


if __name__ == "__main__":
    main(sys.argv)
