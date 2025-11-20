import os
from pathlib import Path
import shutil
import time
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from pipeline.realtime_pipeline import realtime_pipeline
from pipeline.pipeline import pipeline

# -------------------------
# Config
# -------------------------
NUM_CAMERAS = int(input("Number of camera (from 1 - 8): "))
lst_camera_urls = []
for i in range(NUM_CAMERAS):
    camera_url = input("Link of " + str(i + 1) + "th camera: ")
    lst_camera_urls.append(camera_url)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Thread pool để chạy pipeline nặng mà không block server
executor = ThreadPoolExecutor(max_workers=4)

# -------------------------
# FastAPI init
# -------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Realtime streaming
# -------------------------
async def event_generator():
    loop = asyncio.get_running_loop()
    while True:
        # Chạy pipeline trong thread pool để không block server
        result = await loop.run_in_executor(executor, realtime_pipeline, lst_camera_urls)
        # SSE format
        yield f"data: {json.dumps(result)}\n\n"
        await asyncio.sleep(1)  # 1s giữa các frame

@app.get("/realtime_stream")
async def realtime_stream():
    return StreamingResponse(event_generator(), media_type="text/event-stream")

# -------------------------
# -------------------------
@app.post("/upload_video")
async def upload_video(file: UploadFile = File(...)):
    """
    User uploads a video, server runs pipeline(video_path) and returns JSON prediction.
    """
    try:
        # Lưu file tạm
        timestamp = int(time.time())
        video_path = os.path.join(UPLOAD_DIR, f"{timestamp}_{file.filename}")
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Chạy pipeline trong thread pool để không block
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(executor, pipeline, video_path)

        return JSONResponse(result)

    except Exception as e:
        return JSONResponse({"message": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)