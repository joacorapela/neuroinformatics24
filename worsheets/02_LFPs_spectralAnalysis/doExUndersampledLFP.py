import sys
import argparse
import numpy as np
import plotly.graph_objects as go


def sampleContinuousLFP(t, freq=11):  # freq Hz
    LFP = np.sin(2*np.pi*freq*t)
    return LFP


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--LFP_freq", type=float,
                        help="true LFP frequency (Hz)", default=11.0)
    parser.add_argument("--sample_freq", type=float,
                        help="sample frequency (Hz)", default=10.0)
    parser.add_argument("--min_t", type=float,
                        help="minimum time to plot (sec)", default=-10.0)
    parser.add_argument("--max_t", type=float,
                        help="maximum time to plot (sec)", default=10.0)
    parser.add_argument("--fig_filename_pattern", type=str,
                        help="figure filename pattern",
                        default="figures/undersampledLFP.{:s}")
    args = parser.parse_args()

    LFP_freq = args.LFP_freq
    sample_freq = args.sample_freq
    min_t = args.min_t
    max_t = args.max_t
    fig_filename_pattern = args.fig_filename_pattern

    sampled_t = np.arange(min_t, max_t, 1.0/sample_freq)
    sampled_LFP = sampleContinuousLFP(t=sampled_t, freq=LFP_freq)

    fig = go.Figure()
    trace = go.Scatter(x=sampled_t, y=sampled_LFP, mode="lines+markers")
    fig.add_trace(trace)
    fig.update_layout(xaxis=dict(title="t"), yaxis=dict(title="LFP"))

    fig.write_image(fig_filename_pattern.format("png"))
    fig.write_html(fig_filename_pattern.format("html"))

    fig.show()

    breakpoint()


if __name__ == "__main__":
    main(sys.argv)
