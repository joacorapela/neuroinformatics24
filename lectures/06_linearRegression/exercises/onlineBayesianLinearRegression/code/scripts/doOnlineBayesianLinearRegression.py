
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
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
    parser.add_argument("--update_delay", type=float,
                        help="update delay (sec)", default=0.01)
    parser.add_argument("--images_filename", type=str, help="images filename",
                        default="../../data/xSC.dat")
    parser.add_argument("--responses_filename", type=str,
                        help="responses filename",
                        default="../../data/ySC_5spi.dat")
    args = parser.parse_args()

    response_delay_samples = args.response_delay_samples
    prior_precision_coef = args.prior_precision_coef
    likelihood_precision_coef = args.likelihood_precision_coef
    update_delay = args.update_delay
    images_filename = args.images_filename
    responses_filename = args.responses_filename

    images = np.genfromtxt(images_filename)
    responses = np.genfromtxt(responses_filename)
    Phi = np.column_stack((np.ones(len(images)), images))
    image_width = int(np.sqrt(images.shape[1]))
    image_height = image_width

    Phi = Phi[:-response_delay_samples,]
    responses = responses[response_delay_samples:]

    m0 = np.zeros(shape=(images.shape[1]+1,), dtype=np.double)
    S0 = np.diag(np.ones(len(m0), dtype=np.double))
    indices = np.arange(len(m0))

    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1, adjustable="box", aspect=1)
    ax2 = fig.add_subplot(2, 1, 2)

    mn = m0
    Sn = S0
    for n, yn in enumerate(responses):
        mn, Sn = blr.onlineUpdate(mn=mn, Sn=Sn, phi=Phi[n, :], y=yn,
                                  alpha=prior_precision_coef,
                                  beta=likelihood_precision_coef)
        stds = np.sqrt(np.diag(Sn))
        ax1.clear()
        ax1.contourf(mn[1:].reshape((image_width, image_height)))
        title = (r"$\alpha={:.02f},\beta={:.02f},\lambda={:.02f},"
                 "{:d}/{:d}$".format(
                     prior_precision_coef, likelihood_precision_coef,
                     prior_precision_coef/likelihood_precision_coef,
                     n, len(responses)))
        ax1.set_title(title)
        ax2.clear()
        ax2.errorbar(x=indices, y=mn, yerr=1.96*stds)
        ax2.axhline(y=0)
        ax2.set_xlabel("Pixel index")
        ax2.set_ylabel("Pixel value")
        # Note that using time.sleep does *not* work here!
        plt.pause(update_delay)

    breakpoint()


if __name__ == "__main__":
    main(sys.argv)
