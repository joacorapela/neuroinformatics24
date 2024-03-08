import sys
import numpy as np
import scipy.stats
import cv2
import argparse
import ast
sys.path.append("../src")
import tracking_utils
import inference
import computer_vision


def update_frame(frame, cx, cy, f_mean, f_cov, ellipse_quantile,
                 centroid_color, ellipse_start_angle, ellipse_end_angle,
                 filtered_color, ellipse_thickness):
    quantile_value = scipy.stats.chi2.ppf(q=ellipse_quantile, df=2)
    eig_val, eig_vec = np.linalg.eig(f_cov)
    if eig_val[0] < eig_val[1]:
        tmp = eig_val[0]
        eig_val[0] = eig_val[1]
        eig_val[1] = tmp
        tmp = eig_vec[:, 0]
        eig_vec[:, 0] = eig_vec[:, 1]
        eig_vec[:, 1] = tmp
    major_axis_len = 2 * np.sqrt(quantile_value * eig_val[0])
    minor_axis_len = 2 * np.sqrt(quantile_value * eig_val[1])
    ellipse_axes_len = (int(major_axis_len), int(minor_axis_len))
    ellipse_angle = np.arctan(eig_vec[1, 0]/eig_vec[0, 0]) * 180 / np.pi
    if not np.isnan(cx) and not np.isnan(cy):
        frame = cv2.circle(frame, (cx, cy), radius=0, color=centroid_color,
                           thickness=3)
    frame = cv2.circle(frame, f_mean, radius=0,
                       color=filtered_color, thickness=3)
    frame = cv2.ellipse(frame, f_mean, ellipse_axes_len,
                        ellipse_angle, ellipse_start_angle,
                        ellipse_end_angle, filtered_color,
                        ellipse_thickness)
    return frame


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--video_filename", type=str, help="video filename",
        default="../../data/FrameTop_2021-06-03T17-00-00_end001000.avi")
    parser.add_argument(
        "--pixel_thr_value", type=int,
        help="threshold value for pixels", default=50)
    parser.add_argument(
        "--pixel_max_value", type=int, help="maximum value of pixels",
        default=255)
    parser.add_argument(
        "--max_contour_area", type=int, help="maximum contour area",
        default=2000)
    parser.add_argument(
        "--sigma_a", type=float, help="acceleration standard deviation",
        default=1e2)
    parser.add_argument(
        "--sigma_x", type=float, help="x measurement standard deviation",
        default=1e1)
    parser.add_argument(
        "--sigma_y", type=float, help="y measurement standard deviation",
        default=1e1)
    parser.add_argument(
        "--mu0_x", type=float,
        help="x coordinate of position initial condition", default=100)
    parser.add_argument(
        "--mu0_y", type=float,
        help="y coordinate of position initial condition", default=100)
    parser.add_argument(
        "--sqrt_diag_Q0_value", type=float,
        help="standard deviation of initial state component", default=100)
    parser.add_argument(
        "--ellipse_thickness", type=int,
        help="thickness of the 95% confidence ellipse", default=1)
    parser.add_argument(
        "--ellipse_quantile", type=float,
        help="quantile of the 95% confidence ellipse", default=.95)
    parser.add_argument(
        "--ellipse_start_angle", type=int,
        help="start angle of the 95% confidence ellipse", default=0)
    parser.add_argument(
        "--ellipse_end_angle", type=int,
        help="end angle of the 95% confidence ellipse", default=360)
    parser.add_argument(
        "--centroid_color", type=str,
        help="centroid_color", default="(0, 0, 255)")
    parser.add_argument(
        "--filtered_color", type=str,
        help="filtered_color", default="(0, 255, 0)")
    args = parser.parse_args()

    video_filename = args.video_filename
    pixel_thr_value = args.pixel_thr_value
    pixel_max_value = args.pixel_max_value
    max_contour_area = args.max_contour_area
    sigma_a = args.sigma_a
    sigma_x = args.sigma_x
    sigma_y = args.sigma_y
    mu0_x = args.mu0_x
    mu0_y = args.mu0_y
    sqrt_diag_Q0_value = args.sqrt_diag_Q0_value
    ellipse_thickness = args.ellipse_thickness
    ellipse_quantile = args.ellipse_quantile
    ellipse_start_angle = args.ellipse_start_angle
    ellipse_end_angle = args.ellipse_end_angle
    centroid_color = ast.literal_eval(args.centroid_color)
    filtered_color = ast.literal_eval(args.filtered_color)

    # get video
    cap = cv2.VideoCapture(video_filename)
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
    if int(major_ver) < 3:
        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    else:
        fps = cap.get(cv2.CAP_PROP_FPS)

    # get LDS matrices for tracking
    dt = 1.0 / fps
    A, Q, H, R, Qe = tracking_utils.getLDSmatricesForTracking(
        dt=dt, sigma_a=sigma_a, sigma_x=sigma_x, sigma_y=sigma_y)
    mu0 = np.array([[mu0_x, 0, 0, mu0_y, 0, 0]], dtype=np.double).T
    Q0 = np.diag(np.ones(len(mu0))*sqrt_diag_Q0_value**2)
    onlineKF = inference.OnlineKalmanFilter(A=A, Q=Q, mu0=mu0, Q0=Q0, H=H, R=R)

    # dirty hack to compute the background by taking the median of three
    # frames where the mouse is on different positions
    background = computer_vision.get_background(
        cap=cap, frame_indices=[10000, 29000, 25000])
    while cap.isOpened():
        # get new video frame
        ret, frame = cap.read()
        if ret:
            # get mouse centroid (cx, cy)
            cx, cy = computer_vision.get_moving_object_centroid(
                frame=frame, background=background,
                pixel_thr_value=pixel_thr_value,
                pixel_max_value=pixel_max_value,
                max_contour_area=max_contour_area)
        else:
            break

        # estimate the filtered state
        _, _ = onlineKF.predict()
        f_mean, f_cov = onlineKF.update(y=np.array([cx, cy]))

        # update frame with centroid and filter confidence ellipse
        f_mean_pos = np.array([f_mean[0], f_mean[3]])
        f_mean_pos_int = f_mean_pos.flatten().astype(int)
        f_cov_pos = np.array([[f_cov[0, 0], f_cov[0, 3]],
                              [f_cov[3, 0], f_cov[3, 3]]], dtype=np.double)
        frame = update_frame(frame=frame, cx=cx, cy=cy, f_mean=f_mean_pos_int,
                             f_cov=f_cov_pos,
                             ellipse_quantile=ellipse_quantile,
                             centroid_color=centroid_color,
                             ellipse_start_angle=ellipse_start_angle,
                             ellipse_end_angle=ellipse_end_angle,
                             filtered_color=filtered_color,
                             ellipse_thickness=ellipse_thickness)
        cv2.imshow("", frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main(sys.argv)
