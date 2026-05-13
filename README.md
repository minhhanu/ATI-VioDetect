# ATI-VioDetect

End-to-end real-time violence detection system using deep learning, temporal modeling, and Docker-based deployment.

This project combines:
- ResNet50 for spatial feature extraction
- TSM (Temporal Shift Module) for temporal reasoning
- Real-time multi-camera streaming
- Backend/Frontend decoupled architecture
- Docker deployment for scalable inference

---

## 🔍 Research & Engineering Highlights

### Data Leakage Investigation

During experimentation, we discovered severe data leakage issues in the RLVS (Real-Life Violence Situations) dataset.

The original dataset structure allowed highly similar consecutive frames from the same source videos to appear across Train/Validation/Test splits, leading to unrealistically inflated performance.

To validate this issue:

- A Random Forest classifier was trained only on metadata features (FPS, resolution, source structure)
- The model achieved an anomalous F1-score of approximately 0.93
- This strongly suggested leakage between dataset splits

To address this:

- 359 video folders were manually reorganized
- Source-level separation was enforced
- Strict Train/Validation/Test isolation was rebuilt

After correction:
- The system achieved a more realistic F1-score of approximately 0.87

---

## ⚙️ System Architecture

The system uses a decoupled architecture:

### Frontend
- Handles real-time video streaming
- Optimized for high FPS rendering (~60 FPS)

### Backend
- Performs deep learning inference
- Processes a lower number of frames (~3 FPS)
- Optimized to avoid GPU Out-of-Memory (OOM) issues

The deployment supports:
- Up to 8 concurrent camera streams
- Real-time monitoring
- Offline "Deep Analysis" mode for uploaded videos

---

## 🧠 Technologies Used

### AI / ML
- PyTorch
- ResNet50
- TSM (Temporal Shift Module)
- Random Forest
- OpenCV

### Backend
- FastAPI
- Uvicorn

### Frontend
- React
- Vite

### Deployment
- Docker

## 📘 Mục lục
[I. Giới thiệu & Cấu hình đề xuất]
[II. Cách chạy Local]
[III. Cách chạy với Docker]
[IV. Các lỗi thường gặp]

I. Giới thiệu & Cấu hình đề xuất

Link train model AI colab: https://drive.google.com/drive/folders/1TneJrUoO49BuFWTmKps8brZQUrFWuJyN?usp=drive_link
Link Github repo: https://github.com/minhhanu/ATI-VioDetect
Link Dockerhub: https://hub.docker.com/repository/docker/minhvanhanu/ati-docker-files/tags

Slide cũng ở trong folder project này
Em chào thầy ạ
Đây là phần hướng dẫn chạy project

Trong trường hợp docker không chạy được, xin hãy thầy hãy đọc qua ATI_VioDetect/requirements.txt

## II. Chạy Local - Có video hướng dẫn
# 1️⃣ Chạy backend
cd backend
python -m uvicorn main.server:app --reload

Dấu hiệu backend chạy được:

Model được load.

Có thông báo server chạy và địa chỉ server.

Terminal hỏi số lượng camera.

# 2. Chạy frontend
Step 1: cd tới frontend
Step 2: npm install (để có thư mục node_modules)
Step 2: Nhập "npx vite --host --port 5731"

Dấu hiệu frontend chạy được:

Terminal hiện link để mở giao diện.

# 3. Kết nối camera:

- Bọn em thường dùng app IP webcam ở Google play

- Khi nhấn start server thì nó sẽ hiện ra cái ip của camera, trông như thế này: http://192.168.1.60:8080 (Thầy có thể bấm vô link để điều chỉnh camera)
- Mỗi lần bật là app đổi ip nên khúc connect cam vẫn phải thủ công một chút
- Yêu cầu là laptop + điện thoại cùng wifi ạ

- Tuy nhiên, khi copy link camera vào backend và frontend, phải thêm "/video" vào nữa
http://192.168.1.14:8080 => http://192.168.1.14:8080/video 

Terminal backend hiển thị JSON, frontend render được ạ

Thầy có thể xem video hướng dẫn để trực quan hơn

## III. Chạy với Docker

Repo Docker Hub:
https://hub.docker.com/repository/docker/minhvanhanu/ati-docker-files/general

# 1️⃣ Backend

Build image từ source:

cd backend
docker build -t vio-backend .
(Image của em nặng 12GB lận nên có thể crash)

Hoặc pull trực tiếp từ Docker Hub: docker pull minhvanhanu/ati-docker-files:backend

Chạy backend (interactive để nhập số lượng camera): docker run -it --name vio-backend -p 8000:8000 vio-backend

# 2️⃣ Frontend

Build image:

cd frontend
docker build -t vio-frontend .

Hoặc pull image có sẵn:

docker pull minhvanhanu/ati-docker-files:frontend


Chạy frontend:

docker run -p 5731:80 vio-frontend


Mở trình duyệt tới: http://localhost:5731

Sau đó, kết nối camera như trong hướng dẫn Local.
## V. Các lỗi thường gặp

# 1. Port bị chiếm dụng

netstat -ano | findstr "TEN_PORT"
taskkill /PID <PID_NUMBER> /F


# 2. Không gửi/nhận dữ liệu qua API

Kiểm tra frontend:

frontend/App.tsx (fetch API /realtime)

frontend/components/VideoUploader.tsx (fetch API /upload)

Kiểm tra backend: main/server.py

Đảm bảo frontend gọi đúng endpoint server.

# 3. Realtime quá chậm

Lỗi liên quan tới __pycache__.

Giải pháp: chạy backend khoảng 40 JSON (hoặc nhiều hơn), chương trình sẽ đạt hiệu suất ổn định.

# 4. Server không chạy được
- Thường là do 1 trong 2 lỗi sau:
+) Input type mismatch: Num of camera yêu cầu int, nhưng nhập giá trị khác (String...)
+) Link camera không đúng: Khi backend không tìm thấy địa chỉ camera => Không có frame truyền vào server => cv2 found no frame

- Xin thầy đảm bảo link camera đúng (có /video). 
- Với frontend, thầy có thể không nhập hoặc nhập sai
- Nhưng với backend, mọi thứ phải đúng

- Nguyên nhân lỗi: Backend và Frontend kết nối camera độc lập
# Frontend có nhiệm vụ stream, hiển thị FPS cao nhất có thể
# Tuy nhiên, backend mỗi giây chỉ lấy một vài frame

- Em không muốn project bị chồng chéo logic, nên bọn em quyết định thiết kế theo hướng đó

- Cách sửa: Chạy lại server và frontend từ đầu

# 5. Frontend không khởi chạy
- Terminal yêu cầu tải vite@7.2.4
- Lí do: Chưa có node_modules
- Solution: cd frontend => Tải dependencies với lệnh: npm install

## V. Danh sách sinh viên
- 2301040117 - Hoàng Văn Minh

- 2201040121 - Phùng Thị Nga

- 2301040161 - Lê Bảo Quốc

- 220140078 - Phạm Phương Hồng

- 2201040006 - Nguyễn Hoàng Anh

Nếu có vấn đề gì, xin hãy liên hệ với em
# Email: hoangvanminh2100@gmail.com
# Phone number + zalo: 0399593750
# Student ID để liên lạc qua team, qua outlook: 2301040117
# Messenger, facebook: https://www.facebook.com/minh.van.48176/
