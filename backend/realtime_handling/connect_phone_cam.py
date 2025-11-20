import cv2
import time
import numpy as np


def connect_and_stream(camera_url):
    cap = cv2.VideoCapture(camera_url, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        yield (False, None)
        return

    while True:
        ret, frame = cap.read()
        yield (ret, frame)
        if not ret:
            time.sleep(0.1)