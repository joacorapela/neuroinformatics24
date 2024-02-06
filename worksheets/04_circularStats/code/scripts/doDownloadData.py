import os
import sys
import argparse
import numpy as np
from dandi.dandiapi import DandiAPIClient
from pynwb import NWBHDF5IO


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dandiset_id", type=str, help="Dandiset ID",
                        default="000019")
    parser.add_argument("--dandiset_filepath", type=str,
                        help="Dandiset path",
                        default="sub-EC2/sub-EC2_ses-EC2-B105.nwb")
    parser.add_argument("--downsample_factor", type=int,
                        help="downsample factor", default=8)
    parser.add_argument("--electrodes", type=str,
                        help="Electrodes to download",
                        default="[135,136,137,138,139,140,141,142]")
    parser.add_argument("--data_filename_pattern", type=str,
                        help="data filename pattern",
                        default="../../data/{:s}_{:s}_{:s}_{:s}.npz")
    args = parser.parse_args()

    dandiset_id = args.dandiset_id
    dandiset_filepath = args.dandiset_filepath
    downsample_factor = args.downsample_factor
    electrodes_str = args.electrodes
    data_filename_pattern = args.data_filename_pattern

    electrodes = electrodes_str[1:-1].split(",")
    electrodes = np.array([int(electrode) for electrode in electrodes])

    with DandiAPIClient() as client:
        asset = client.get_dandiset(dandiset_id, "draft").get_asset_by_path(
            dandiset_filepath)
        s3_path = asset.get_content_url(follow_redirects=1, strip_query=True)

    # Open the file in read mode "r", and specify the driver as "ros3" for
    # S3 files
    io = NWBHDF5IO(s3_path, mode="r", driver="ros3")
    nwbfile = io.read()

    trials = nwbfile.trials.to_dataframe()
    cvs_transition_times = trials["cv_transition_time"]

    srate = nwbfile.acquisition["ElectricalSeries"].rate
    print(f"Getting electodes {electrodes_str} data")
    voltages = nwbfile.acquisition["ElectricalSeries"].data[:, electrodes-1]
    print(f"Done getting electodes {electrodes_str} data")

    dandiset_path = os.path.splitext(os.path.basename(dandiset_filepath))[0]
    data_filename = data_filename_pattern.format(dandiset_id, dandiset_path,
                                                 electrodes_str,
                                                 f"DS{downsample_factor}")
    dirname = os.path.dirname(data_filename)
    if not os.path.exists(dirname):
        print(f"Creating directory {dirname}")
        os.mkdir(dirname)
    np.savez(data_filename, cvs_transition_times=cvs_transition_times,
             srate=srate, voltages=voltages.T, electrodes=electrodes)
    print(f"Data downloaded to {data_filename}")

    breakpoint()


if __name__ == "__main__":
    main(sys.argv)
