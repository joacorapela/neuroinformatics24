import os
import sys
import argparse
import numpy as np
import scipy.signal


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--narrowband_voltages_filename", type=str,
                        help="data filename",
                        default=("../../results/000019_sub-EC2_ses-EC2-B105_"
                                 "[135,136,137,138,139,140,141,142]_"
                                 "0.4-0.8Hz.npz"))
    args = parser.parse_args()

    narrowband_voltages_filename = args.narrowband_voltages_filename
    file_descriptor = os.path.splitext(narrowband_voltages_filename)[0]
    results_filename = file_descriptor + "_HT.npz"

    load_res = np.load(narrowband_voltages_filename)
    filtered_voltages = load_res["filtered_voltages"]
    ht_filtered_voltages = scipy.signal.hilbert(
        x=filtered_voltages)
    srate = load_res["srate"]
    electrodes = load_res["electrodes"]
    cvs_transition_times = load_res["cvs_transition_times"]

    np.savez(results_filename, cvs_transition_times=cvs_transition_times,
             srate=srate, electrodes=electrodes,
             ht_filtered_voltages=ht_filtered_voltages)
    print(f"Hilbert transformed data saved to {results_filename}")

    breakpoint()


if __name__ == "__main__":
    main(sys.argv)
