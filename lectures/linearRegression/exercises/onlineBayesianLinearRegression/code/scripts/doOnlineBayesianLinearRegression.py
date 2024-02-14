
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import joacorapela_common.stats.bayesianLinearRegression as blr


def main(argv):
    parser = argparse.ArgumentParser()
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

    prior_precision_coef = args.prior_precision_coef
    likelihood_precision_coef = args.likelihood_precision_coef
    update_delay = args.update_delay
    images_filename = args.images_filename
    responses_filename = args.responses_filename

    images = np.genfromtxt(images_filename)
    responses = np.genfromtxt(responses_filename)
    Phi = np.column_stack((np.ones(len(images)), images))
    image_width = int(np.sqrt(images.shape[1]))
    image_heigth = image_width

    m0 = np.zeros(shape=(images.shape[1]+1,), dtype=np.double)
    S0 = np.diag(np.ones(len(m0), dtype=np.double))
    indices = np.arange(len(m0))

    fig, ax = plt.subplots(nrows=2, ncols=1)

    mn = m0
    Sn = S0
    for n, yn in enumerate(responses):
        mn, Sn = blr.onlineUpdate(mn=mn, Sn=Sn, phi=Phi[n, :], y=yn,
                                  alpha=prior_precision_coef,
                                  beta=likelihood_precision_coef)
        stds = np.sqrt(np.diag(Sn))
        ax[0].clear()
        ax[0].imshow(mn[1:].reshape((image_width, image_heigth)))
        title = (r"$\alpha={:.02f},\beta={:.02f},\lambda={:.02f},"
                 "{:d}/{:d}$".format(
                     prior_precision_coef, likelihood_precision_coef,
                     prior_precision_coef/likelihood_precision_coef,
                     n, len(responses)))
        ax[0].set_title(title)
        ax[1].clear()
        ax[1].errorbar(x=indices, y=mn, yerr=1.96*stds)
        ax[1].axhline(y=0)
        ax[1].set_xlabel("Pixel index")
        ax[1].set_ylabel("Pixel value")
        # Note that using time.sleep does *not* work here!
        plt.pause(update_delay)
    breakpoint()


if __name__ == "__main__":
    main(sys.argv)
