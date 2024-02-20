
import sys
import argparse
import numpy as np
import pandas as pd
import plotly.graph_objects as go

import utils


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--snr", type=float,
                        help="responses snr",
                        default=1.0)
    parser.add_argument("--images_filename", type=str,
                        help="images filename",
                        default="http://www.gatsby.ucl.ac.uk/~rapela/neuroinformatics/2024/worksheets/linearRegression/data/xCC.dat")
    parser.add_argument("--responses_filename", type=str,
                        help="simulated responses filename",
                        default="../../results/ySimCC.dat")
    parser.add_argument("--figures_filename_pattern", type=str,
                        help="figures filename pattern",
                        default="../../figures/ySimCC.{:s}")
    args = parser.parse_args()

    # get command line parameters
    snr = args.snr
    images_filename = args.images_filename
    responses_filename = args.responses_filename
    figures_filename_pattern = args.figures_filename_pattern

    # get data
    images = pd.read_csv(images_filename, sep=" ").to_numpy()

    # get noise from snr
    std_noise = np.mean(np.abs(images)) / snr

    # compute basis functions and projections of images onto them
    gabor0 = utils.gabor(sigma=1.5, theta=np.pi/4, Lambda=1, psi=0,
                         gamma=1).flatten()
    gabor1 = utils.gabor(sigma=1.5, theta=np.pi/4, Lambda=1, psi=np.pi/2,
                         gamma=1).flatten()
    rds = np.zeros(shape=(images.shape[1], 2), dtype=np.double)
    rds[0:len(gabor0), 0] = gabor0
    rds[0:len(gabor1), 1] = gabor1

    # simulate responses
    noise = np.random.normal(loc=0, scale=std_noise, size=images.shape[0])
    noiseless_responses = (images @ rds[:, 0])**2 + (images @ rds[:, 1])**2
    responses = noiseless_responses + noise
    responses[responses < 0] = 0.0

    # save responses
    df = pd.DataFrame(responses)
    df.to_csv(responses_filename)
    print(f"Simulation written to {responses_filename}")

    # plot responses
    fig = go.Figure()
    trace = go.Scatter(x=np.arange(len(responses)), y=responses,
                       mode="markers", name="responses")
    fig.add_trace(trace)
    trace = go.Scatter(x=np.arange(len(noiseless_responses)),
                       y=noiseless_responses,
                       mode="markers", name="noiseless_responses")
    fig.add_trace(trace)
    fig.update_layout(xaxis=dict(title="Index"), yaxis=dict(title="Response"))
    fig.write_image(figures_filename_pattern.format("png"))
    fig.write_html(figures_filename_pattern.format("html"))
    fig.show()

    breakpoint()


if __name__ == "__main__":
    main(sys.argv)
