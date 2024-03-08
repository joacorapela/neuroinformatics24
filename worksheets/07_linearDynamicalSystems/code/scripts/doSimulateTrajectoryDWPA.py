
"""
Sampling from a Discrete Wiener Process Acceleration Model
==========================================================

The code below samples from a Discrete Wiener Process Acceleration (DWPA)
model.

"""

import sys
import os
import argparse
import numpy as np
import plotly.graph_objs as go
sys.path.append("../src")
import tracking_utils
import simulation


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--pos_x0", type=float,
                        help="Initial position x value", default=0.0)
    parser.add_argument("--pos_y0", type=float,
                        help="Initial position y value", default=0.0)
    parser.add_argument("--vel_x0", type=float,
                        help="initial velocity x value", default=0.0)
    parser.add_argument("--vel_y0", type=float,
                        help="initial velocity y value", default=0.0)
    parser.add_argument("--acc_x0", type=float,
                        help="initial acceleration x value", default=0.0)
    parser.add_argument("--acc_y0", type=float,
                        help="initial acceleration y value", default=0.0)
    parser.add_argument("--dt", type=float, help="sampling period",
                        default=1e-3)
    parser.add_argument("--num_pos", type=int, help="sampling period",
                        default=1000)
    parser.add_argument("--sigma_a", type=float,
                        help="standard deviation of acceleration", default=1.0)
    parser.add_argument("--sigma_x", type=float,
                        help=("standard deviation of the x component of "
                              "accelerations"), default=1.0)
    parser.add_argument("--sigma_y", type=float,
                        help=("standard deviation of the y component of "
                              "accelerations"), default=1.0)
    parser.add_argument("--sqrt_diag_P0_value", type=float,
                        help="standard deviation of initial state components",
                        default=1e-3)
    args = parser.parse_args()

    pos_x0 = args.pos_x0
    pos_y0 = args.pos_y0
    vel_x0 = args.vel_x0
    vel_y0 = args.vel_y0
    acc_x0 = args.acc_x0
    acc_y0 = args.acc_y0
    dt = args.dt
    num_pos = args.num_pos
    sigma_a = args.sigma_a
    sigma_x = args.sigma_x
    sigma_y = args.sigma_y
    sqrt_diag_P0_value = args.sqrt_diag_P0_value

    # Set LDS parameters
    A, Q, H, R, Qe = tracking_utils.getLDSmatricesForTracking(
        dt=dt, sigma_a=sigma_a, sigma_x=sigma_x, sigma_y=sigma_y)
    R = np.diag([sigma_x**2, sigma_y**2])
    mu0 = np.array([pos_x0, vel_x0, acc_x0, pos_y0, vel_y0, acc_y0],
                   dtype=np.double)
    P0 = np.diag(np.ones(len(mu0))*sqrt_diag_P0_value**2)

    # Sample from the LDS
    x0, x, y = simulation.simulateLDS(N=num_pos, A=A, Q=Q, H=H, R=R, mu0=mu0,
                                      P0=P0)

    # Plot state positions and measurements
    fig = go.Figure()
    trace_x = go.Scatter(x=x[0, :], y=x[3, :], mode="markers",
                         showlegend=True, name="state position")
    trace_y = go.Scatter(x=y[0, :], y=y[1, :], mode="markers",
                         showlegend=True, name="measured position",
                         opacity=0.3)
    trace_start = go.Scatter(x=[x0[0]], y=[x0[3]], mode="markers",
                             text="initial state position", marker={"size": 7},
                             showlegend=False)
    fig.add_trace(trace_x)
    fig.add_trace(trace_y)
    fig.add_trace(trace_start)
    fig_filename_pattern = "../../figures/simulated_pos.{:s}"
    png_filename = fig_filename_pattern.format("png")
    dirname = os.path.dirname(png_filename)
    if not os.path.exists(dirname):
        print(f"Creating directory {dirname}")
        os.mkdir(dirname)
    fig.write_image(png_filename)
    html_filename = fig_filename_pattern.format("html")
    fig.write_html(html_filename)
    fig.show()


if __name__ == "__main__":
    main(sys.argv)
