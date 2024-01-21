import os
import sys
import argparse
import numpy as np
import plotly.graph_objects as go

import utils


def test_func(t, f0):
    answer = np.sinc(f0 * t)**2
    return answer


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--f0", type=float, help="sinc maximal frequency",
                        default=2.0)
    parser.add_argument("--fs_factor", type=float,
                        help="sampling frequency factor of the Nyquist rate",
                        default=1.0)
    parser.add_argument("--xmin", type=float, help="minimum x value",
                        default=-2.5)
    parser.add_argument("--nXs_fine_grained", type=int,
                        help="number of fine grained abscissa points",
                        default=1000)
    parser.add_argument("--fig_filename_pattern", type=str,
                        help="figure filename pattern",
                        default="figures/example_fsFactor{:.2f}.{:s}")
    args = parser.parse_args()

    f0 = args.f0
    fs_factor = args.fs_factor
    xmin = args.xmin
    nXs_fine_grained = args.nXs_fine_grained
    fig_filename_pattern = args.fig_filename_pattern

    Nyquist_rate = 2 * f0

    # function from which samples will be drawn sampled at a high frequency
    t_original = np.linspace(xmin, -xmin, nXs_fine_grained)
    func_values_original = test_func(t=t_original, f0=f0)

    # sample at Nyquist factor * Niquist rate
    f_sample = fs_factor * Nyquist_rate
    t_sampled = np.arange(xmin, -xmin, 1/f_sample)
    func_values_sampled = test_func(t=t_sampled, f0=f0)

    # reconstruct
    t_reconstructed = np.linspace(xmin, -xmin, nXs_fine_grained)
    func_values_reconstructed = utils.wittakerShannonInterpolator(
        t=t_reconstructed, ys=func_values_sampled, fs=f_sample)

    # plot
    fig = go.Figure()
    trace_original = go.Scatter(x=t_original, y=func_values_original,
                                mode="lines+markers", name="original")
    trace_sampled = go.Scatter(x=t_sampled, y=func_values_sampled,
                               mode="markers", name="sampled")
    trace_reconstructed = go.Scatter(x=t_reconstructed,
                                     y=func_values_reconstructed,
                                     mode="lines+markers",
                                     name="reconstructed")
    fig.add_trace(trace_original)
    fig.add_trace(trace_sampled)
    fig.add_trace(trace_reconstructed)
    fig.update_layout(title=f"fs={fs_factor}*Nyquist rate",
                      xaxis=dict(title="t (sec)"), yaxis=dict(title="x(t)"))

    filename = fig_filename_pattern.format(fs_factor, "png")
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        print(f"Creating directory {dirname}")
        os.mkdir(dirname)
    fig.write_image(filename)
    fig.write_html(fig_filename_pattern.format(fs_factor, "html"))

    fig.show()

    breakpoint()


if __name__ == "__main__":
    main(sys.argv)
