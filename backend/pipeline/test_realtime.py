from pipeline.realtime_pipeline import realtime_pipeline

CAMERA_URL = "http://192.168.1.14:8080/video"
NUM_CAMERAS = 8
lst_camera_urls = [CAMERA_URL for _ in range(NUM_CAMERAS)]

while True:
    realtime_pipeline(lst_camera_urls=lst_camera_urls)