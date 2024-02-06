import os
import sys
import argparse
import numpy as np
import scipy.signal


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_filename", type=str,
                        help="data filename",
                        default=("../../data/000019_sub-EC2_ses-EC2-B105_"
                                 "[135,136,137,138,139,140,141,142].npz"))
    parser.add_argument("--low_cutoff", type=float,
                        help="low-frequency cutoff of butterworth filter",
                        default=0.4)
    parser.add_argument("--high_cutoff", type=float,
                        help="high-frequency cutoff of butterworth filter",
                        default=0.8)
    parser.add_argument("--butter_order", type=int,
                        help="order of butterworth filter", default=2)
    parser.add_argument("--butter_type", type=str,
                        help="type of butterworth filter", default="bandpass")
    parser.add_argument("--results_filename_pattern", type=str,
                        help="results filename pattern",
                        default="../../results/{:s}_{:s}.npz")
    args = parser.parse_args()

    data_filename = args.data_filename
    low_cutoff = args.low_cutoff
    high_cutoff = args.high_cutoff
    butter_order = args.butter_order
    butter_type = args.butter_type
    results_filename_pattern = args.results_filename_pattern

    file_descriptor = os.path.splitext(os.path.basename(data_filename))[0]
    results_filename = results_filename_pattern.format(
        file_descriptor, f"{low_cutoff}-{high_cutoff}Hz")
    dirname = os.path.dirname(results_filename)
    if not os.path.exists(dirname):
        print(f"Creating directory {dirname}")
        os.mkdir(dirname)

    load_res = np.load(data_filename)
    voltages = load_res["voltages"]
    srate = load_res["srate"]
    electrodes = load_res["electrodes"]
    cvs_transition_times = load_res["cvs_transition_times"]

    butter_freqs = 2 * np.array([low_cutoff, high_cutoff]) / srate
    b, a = scipy.signal.butter(N=butter_order, Wn=butter_freqs,
                               btype=butter_type)
    filtered_voltages = scipy.signal.filtfilt(b=b, a=a, x=voltages)
    np.savez(results_filename, cvs_transition_times=cvs_transition_times,
             srate=srate, electrodes=electrodes,
             filtered_voltages=filtered_voltages)
    print(f"Filtered data saved to {results_filename}")


if __name__ == "__main__":
    main(sys.argv)
