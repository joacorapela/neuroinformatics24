
import numpy as np
import cv2


def get_background(cap, frame_indices):
    num_frames = len(frame_indices)
    frames = None
    for i, idx in enumerate(frame_indices):
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if i == 0:
            frames = np.empty((frame.shape[0], frame.shape[1], frame.shape[2],
                               num_frames), dtype=np.int8)
        frames[:, :, :, i] = frame
    median_frame = np.median(frames, axis=-1).astype(np.uint8)
    background = cv2.cvtColor(median_frame, cv2.COLOR_BGR2GRAY)
    return background


def get_moving_object_centroid(frame, background, pixel_thr_value,
                               pixel_max_value, max_contour_area):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_diff = cv2.absdiff(frame_gray, background)
    ret, frame_thr = cv2.threshold(frame_diff, pixel_thr_value,
                                   pixel_max_value, cv2.THRESH_BINARY)
    contours, hiearchy = cv2.findContours(frame_thr,
                                          cv2.RETR_EXTERNAL,
                                          cv2.CHAIN_APPROX_SIMPLE)
    cx, cy = np.nan, np.nan
    if len(contours) > 0:
        contour_areas = np.empty(len(contours), dtype=np.int32)
        for i, contour in enumerate(contours):
            contour_areas[i] = cv2.contourArea(contour)
        max_contour_area_index = np.argmax(contour_areas)
        if contour_areas[max_contour_area_index] < max_contour_area:
            M = cv2.moments(contours[max_contour_area_index])
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
    return cx, cy
