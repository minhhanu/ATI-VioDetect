# ATI-VioDetect

An end-to-end, real-time violence detection system utilizing deep learning, temporal modeling, and Docker-based deployment. 

The system features a decoupled frontend-backend architecture designed for scalable inference and multi-camera stream processing.

---

### 🔗 Project Resources
* **Production Images:** [Docker Hub Repository](https://hub.docker.com/repository/docker/minhvanhanu/ati-docker-files/tags)
* **Model Training:** [Google Drive - Google Colab Notebooks](https://drive.google.com/drive/folders/1TneJrUoO49BuFWTmKps8brZQUrFWuJyN?usp=drive_link)
* **Presentation:** Project Slides are included within the root directory.

---
## 🔍 Research & Engineering Highlights

### Data Leakage Investigation
During experimentation with the **RLVS (Real-Life Violence Situations)** dataset, a severe data leakage issue was identified. The original dataset structure allowed highly similar consecutive frames from the same source videos to appear across the Train, Validation, and Test splits, leading to artificially inflated performance metrics.

**Validation Strategy:**
* A Random Forest classifier was trained **solely on metadata features** (such as FPS, resolution, video source structure).
* The model achieved an anomalous **F1-score of ~0.93**, mathematically proving the existence of information leakage between dataset splits.

**Resolution & Mitigation:**
* Manually reorganized **359 video folders** to enforce strict source-level separation.
* Rebuilt isolated Train/Validation/Test splits using greedy algorithm

## ⚙️ System Architecture

The system utilizes a decoupled architecture to isolate UI rendering logic from heavy AI inference, effectively preventing GPU Out-of-Memory (OOM) errors.

* **Frontend:** Handles real-time UI rendering and multi-camera stream display, optimized for high responsiveness (**~60 FPS**).
* **Backend:** Executes deep learning inference on sampled frames (**~3 FPS**) to optimize compute resource allocation.
* **Scalability:** Supports up to **8 concurrent camera streams**, real-time monitoring, and an offline "Deep Analysis" mode for video uploads.

---

## 🧠 Technologies Used

* **AI / ML:** PyTorch, ResNet50, TSM (Temporal Shift Module), Random Forest, OpenCV
* **Backend:** FastAPI, Uvicorn
* **Frontend:** React, Vite, TypeScript
* **DevOps & Deployment:** Docker, Docker Hub

---

## 🚀 Getting Started

### Option 1: Local Development Setup

#### 1. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main.server:app --reload
```
##### Note: Upon initialization, the backend will prompt for the number of concurrent camera streams.
#### 2. Frontend setup
```bash
cd frontend
npm install
npx vite --host --port 5731
```
#### 3. IP Camera Integration
To connect external camera streams (e.g., using IP Webcam applications via Android/iOS):
Ensure both the host machine and the mobile device are connected to the same local network (Wi-Fi).
Obtain the RTSP/HTTP stream URL from the application (e.g., http://192.168.1.14:8080).
Append the video suffix /video to the stream endpoint when configuring the source: http://192.168.1.14:8080/video.

### Option 2: Docker Deployment
#### 1. Pre-built image
```bash
# Pull and run Backend
docker pull minhvanhanu/ati-docker-files:backend
docker run -it --name vio-backend -p 8000:8000 minhvanhanu/ati-docker-files:backend

# Pull and run Frontend
docker pull minhvanhanu/ati-docker-files:frontend
docker run -p 5731:80 minhvanhanu/ati-docker-files:frontend
```
#### 2. Building from Source
```bash
# Backend
cd backend
docker build -t vio-backend .
docker run -it --name vio-backend -p 8000:8000 vio-backend

# Frontend
cd frontend
docker build -t vio-frontend .
docker run -p 5731:80 vio-frontend
```
Access the application web interface at: http://localhost:5731

## 🛠️ Troubleshooting & Core Mechanics

| Issue | Root Cause | Solution / Workaround |
| :--- | :--- | :--- |
| **Port Collision** | Port `5731` or `8000` is already in use by another process. | Terminate the occupying process using `taskkill /PID <PID> /F` after identifying it via `netstat -ano`. |
| **API Connection Failure** | Mismatched URL endpoints between services. | Verify the target endpoints in `frontend/App.tsx` (`/realtime`) and `frontend/components/VideoUploader.tsx` (`/upload`) match the FastAPI server configuration. |
| **Input Type Mismatch** | Non-integer value passed to the backend camera configuration prompt. | Restart the backend service and ensure the camera count input is a valid integer. |
| **Empty Frame / Inference Crash** | Invalid IP Camera URL or dropped network packets. | Ensure the stream URL includes the correct streaming suffix (`/video`) and that the host machine can ping the camera IP. |

---

## 👥 Contributors

* **Hoàng Văn Minh** (Project Lead & Core Engineer) - `hoangvanminh2100@gmail.com`
* Phùng Thị Nga
* Lê Bảo Quốc
* Phạm Phương Hồng
* Nguyễn Hoàng Anh

---
*For technical inquiries or collaboration, please contact the Project Lead via Email or GitHub Issues.*
