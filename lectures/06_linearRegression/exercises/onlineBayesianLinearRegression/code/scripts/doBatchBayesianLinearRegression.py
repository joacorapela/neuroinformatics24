
import sys
import argparse
import numpy as np
import pandas as pd
import plotly.subplots
import plotly.graph_objects as go
import joacorapela_common.stats.bayesianLinearRegression as blr


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--response_delay_samples", type=int,
                        help=("we associate each response to the image "
                              "presented response_delay_samples in the past"),
                        default=1)
    parser.add_argument("--prior_precision_coef", type=float,
                        help="prior precision coefficient",
                        default=0.5)
    parser.add_argument("--likelihood_precision_coef", type=float,
                        help="likelihood precision coefficient",
                        default=0.1)
    parser.add_argument("--images_filename", type=str, help="images filename",
                        default="../../data/xSC.dat")
    parser.add_argument("--responses_filename", type=str,
                        help="responses filename",
                        default="../../data/ySC_5spi.dat")
    args = parser.parse_args()

    response_delay_samples = args.response_delay_samples
    prior_precision_coef = args.prior_precision_coef
    likelihood_precision_coef = args.likelihood_precision_coef
    images_filename = args.images_filename
    responses_filename = args.responses_filename

    images = pd.read_csv(images_filename, sep="\s+").to_numpy()
    responses = pd.read_csv(responses_filename, sep="\s+").to_numpy().flatten()
    Phi = np.column_stack((np.ones(len(images)), images))
    image_width = int(np.sqrt(images.shape[1]))
    image_height = image_width

    Phi = Phi[:-response_delay_samples,]
    responses = responses[response_delay_samples:]

    mN, SN = blr.batchWithSimplePrior(Phi=Phi, y=responses,
                                      alpha=prior_precision_coef,
                                      beta=likelihood_precision_coef)
    # plot RFs
    x_grid = np.arange(0, image_width, 1)
    y_grid = np.arange(0, image_height, 1)
    X_grid, Y_grid = np.meshgrid(x_grid, y_grid)

    mN_2D = np.reshape(mN[1:], (image_height, image_width))

    fig = plotly.subplots.make_subplots(rows=2, cols=1)

    trace = go.Contour(x=x_grid, y=y_grid, z=mN_2D, showscale=False)
    fig.add_trace(trace, row=1, col=1)
    fig.update_yaxes(scaleanchor="x", scaleratio=1, row=1, col=1)

    trace = go.Scatter(x=np.arange(len(mN)), y=mN,
                       error_y=dict(type="data", array=np.diag(SN),
                                    visible=True))
    fig.add_trace(trace, row=2, col=1)
    fig.add_hline(y=0, row=2, col=1)

    fig.show()

    breakpoint()


if __name__ == "__main__":
    main(sys.argv)
