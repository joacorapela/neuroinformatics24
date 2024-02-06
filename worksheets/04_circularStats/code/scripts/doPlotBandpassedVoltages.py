import os
import sys
import argparse
import numpy as np
import plotly.graph_objects as go


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--plot_start_time", type=float,
                        help="plot start time", default=390)
    parser.add_argument("--plot_end_time", type=float, help="plot end time",
                        default=400)
    parser.add_argument("--narrowband_voltages_filename", type=str,
                        help="data filename",
                        default=("../../results/000019_sub-EC2_ses-EC2-B105_"
                                 "[135,136,137,138,139,140,141,142]_"
                                 "0.4-0.8Hz.npz"))
    parser.add_argument("--fig_filename_pattern", type=str,
                        help="results filename pattern",
                        default="../../figures/{:s}.{:s}")
    args = parser.parse_args()

    plot_start_time = args.plot_start_time
    plot_end_time = args.plot_end_time
    narrowband_voltages_filename = args.narrowband_voltages_filename
    fig_filename_pattern = args.fig_filename_pattern

    load_res = np.load(narrowband_voltages_filename)
    filtered_voltages = load_res["filtered_voltages"]
    srate = load_res["srate"]
    electrodes = load_res["electrodes"]

    times = np.arange(filtered_voltages.shape[1]) / srate
    plot_start_sample = np.argmin(np.abs(times-plot_start_time))
    plot_end_sample = np.argmin(np.abs(times-plot_end_time))
    times = times[plot_start_sample:plot_end_sample]
    filtered_voltages = filtered_voltages[:, plot_start_sample:plot_end_sample]
    max_filtered_voltages = np.max(filtered_voltages, axis=1)
    max_filtered_voltages = np.expand_dims(max_filtered_voltages, 1)
    filtered_voltages = filtered_voltages/max_filtered_voltages

    fig = go.Figure()
    for i in range(filtered_voltages.shape[0]):
        trace = go.Scatter(x=times, y=filtered_voltages[i, :], mode="lines",
                           name=f"{electrodes[i]}")
        fig.add_trace(trace)
    fig.update_layout(xaxis=dict(title="Time (sec)"),
                      yaxis=dict(title="Voltage (Voltz)"))

    file_descriptor = os.path.splitext(os.path.basename(
        narrowband_voltages_filename))[0]
    file_descriptor += "_voltages"
    png_fig_filename = fig_filename_pattern.format(file_descriptor, "png")
    html_fig_filename = fig_filename_pattern.format(file_descriptor, "html")
    dirname = os.path.dirname(png_fig_filename)
    if not os.path.exists(dirname):
        print(f"Creating directory {dirname}")
        os.mkdir(dirname)
    fig.write_image(png_fig_filename)
    fig.write_html(html_fig_filename)

    breakpoint()


if __name__ == "__main__":
    main(sys.argv)
