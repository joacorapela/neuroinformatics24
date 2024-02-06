import sys
import argparse
import numpy as np
import scipy.signal
import astropy.stats
from dandi.dandiapi import DandiAPIClient
from pynwb import NWBHDF5IO
import plotly.graph_objects as go


def calculateMeanResultantVector(angles):
    vectors = np.array([np.exp(1j*angle) for angle in angles])
    mean_resultant_vector = vectors.mean()
    return mean_resultant_vector


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dandiset_id", type="str", help="Dandiset ID",
                        default="000019")
    parser.add_argument("--filepath", type="str", help="Dandiset path",
                        default="sub-EC2/sub-EC2_ses-EC2-B105.nwb")
    electrode = 144
    low_cutoff = 0.4
    high_cutoff = 0.8
    butter_order = 2.0
    butter_type = "bandpass"
    n_circ_bins = 10

    with DandiAPIClient() as client:
        asset = client.get_dandiset(dandiset_id, "draft").get_asset_by_path(
            filepath)
        s3_path = asset.get_content_url(follow_redirects=1, strip_query=True)

    # Open the file in read mode "r", and specify the driver as "ros3" for
    # S3 files
    io = NWBHDF5IO(s3_path, mode="r", driver="ros3")
    nwbfile = io.read()

    trials = nwbfile.trials.to_dataframe()
    cvs_transition_times = trials["cv_transition_time"]

    srate = nwbfile.acquisition["ElectricalSeries"].rate
    print(f"Getting electode {electrode} data")
    elect_voltages = nwbfile.acquisition["ElectricalSeries"].\
        data[:, electrode-1]
    print(f"Getting electode {electrode} data done")
    times = np.arange(0, len(elect_voltages)) / srate
    cvs_trans_samples = [np.argmin(np.abs(times-cvs_transition_time))
                         for cvs_transition_time in cvs_transition_times]
    butter_freqs = 2 * np.array([low_cutoff, high_cutoff]) / srate
    b, a = scipy.signal.butter(N=butter_order, Wn=butter_freqs,
                               btype=butter_type)
    elect_voltages_filtered = scipy.signal.filtfilt(b=b, a=a, x=elect_voltages)
    elect_voltages_filtered_hilbert = scipy.signal.hilbert(
        x=elect_voltages_filtered)
#     elect_voltages_filtered_hilbert_envelope = np.abs(
#         elect_voltages_filtered_hilbert)
    elect_voltages_filtered_hilbert_phases = np.angle(
        elect_voltages_filtered_hilbert)
    cvs_transition_phases = elect_voltages_filtered_hilbert_phases[
        cvs_trans_samples]

    p_value = astropy.stats.rayleightest(cvs_transition_phases)
    print(f"p_value={p_value}")

#     fig = go.Figure()
#     trace = go.Scatter(x=times, y=elect_voltages_filtered, name="filtered")
#     fig.add_trace(trace)
#     trace = go.Scatter(x=times, y=elect_voltages_filtered_hilbert_envelope,
#                        name="envelop")
#     fig.add_trace(trace)
#     fig.update_layout(xaxis=dict(title="Time (sec)"),
#                       yaxis=dict(title="Voltage (Voltz)"))
#     fig.show()

    mean_resultant_vector = calculateMeanResultantVector(
        angles=cvs_transition_phases)
    mean_resultant_vector_angle_degrees = (np.angle(mean_resultant_vector) * 360.0 / (2 * np.pi))
    cvs_transition_phases_degrees = 360 / (2 * np.pi) * cvs_transition_phases

    fig = go.Figure()
    trace = go.Scatterpolar(r=np.ones(len(cvs_transition_phases_degrees)),
                            theta=cvs_transition_phases_degrees,
                            mode="markers")
    fig.add_trace(trace)
    trace = go.Scatterpolar(r=[0.0, np.abs(mean_resultant_vector)],
                            theta=[0.0, mean_resultant_vector_angle_degrees],
                            mode="lines")
    fig.add_trace(trace)
    fig.show()

    circ_values, circ_edges = np.histogram(cvs_transition_phases,
                                           bins=n_circ_bins)
    circ_centers = circ_edges[:-1] + np.diff(circ_edges)
    circ_centers_degrees = [circ_center * 360.0 / (2 * np.pi)
                            for circ_center in circ_centers]
    fig = go.Figure()
    trace = go.Barpolar(r=circ_values, theta=circ_centers_degrees,
                        width=360.0/len(circ_centers))
    fig.add_trace(trace)
    fig.show()

    breakpoint()


if __name__ == "__main__":
    main(sys.argv)
