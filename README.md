## 📘 Mục lục
[I. Giới thiệu & Cấu hình đề xuất]
[II. Cách chạy Local]
[III. Cách chạy với Docker]
[IV. Các lỗi thường gặp]

I. Giới thiệu & Cấu hình đề xuất
Link train model AI colab: https://drive.google.com/drive/folders/1TneJrUoO49BuFWTmKps8brZQUrFWuJyN?usp=drive_link
Slide cũng ở trong folder project luôn ạ
Em chào thầy ạ
Đây là phần hướng dẫn chạy project ạ

# Note: 
Model (ResNet50 + TSM) sẽ mặc định dùng GPU để xử lí
Laptop của em: Gigabyte G5
Operating system: Window 11
RAM: 8GB

GPU: NVIDIA GeForce RTX 3050 Laptop

CPU: 12th Gen Intel(R) Core(TM) i5-12500H (2.50 GHz)

Để chạy dự đoán bạo lực realtime, nên đảm bảo cấu hình tương đương.

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

- Khi nhấn start server thì nó sẽ hiện ra cái ip của camera, trông như thế này: http://192.168.1.14:8080 (Thầy có thể bấm vô link để điều chỉnh)
- Khi nhấn start server thì nó sẽ hiện ra cái ip của camera, trông như thế này: http://192.168.1.60:8080 (Thầy có thể bấm vô link để điều chỉnh camera)
- Mỗi lần bật là app đổi ip nên khúc connect cam vẫn phải thủ công một chút
- Yêu cầu là laptop + điện thoại cùng wifi ạ

- Tuy nhiên, khi copy link camera vào backend và frontend, phải thêm "/video" vào nữa
http://192.168.1.14:8080 => http://192.168.1.14:8080/video 

Terminal backend hiển thị JSON, frontend render được là OK.

Xem video hướng dẫn để minh họa trực quan hơn.

## III. Chạy với Docker

Repo Docker Hub:
https://hub.docker.com/repository/docker/minhvanhanu/ati-docker-files/general

# 1️⃣ Backend

Build image từ source:

cd backend
docker build -t vio-backend .
(Image của em nặng 12GB lận nên có thể crash)

Hoặc pull trực tiếp từ Docker Hub:

docker pull minhvanhanu/ati-docker-files:backend


Chạy backend (interactive để nhập số lượng camera):

docker run -it --name vio-backend -p 8000:8000 vio-backend


Test backend:

docker exec -it <container_id> python -c "import torch; print(torch.__version__, torch.cuda.is_available())"


Output mong muốn: 2.1.0 True

Nếu dùng NVIDIA docker:

docker run --gpus all -p 8000:8000 vio-backend

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

## IV. Thư viện và phiên bản sử dụng (trường hợp không chạy được Docker)
# 1️⃣ Backend

Python & pip:

Python 3.11.9

pip 25.3

numpy 2.1.3

Các thư viện chính:

fastapi 0.121.1

uvicorn 0.38.0

opencv-python 4.12.0.88

tqdm 4.67.1

ffmpeg-python 0.2.0

python-multipart 0.0.20

Local module (project-specific):

Thư mục tsm/temporal-shift-module/ops chứa các class TemporalShift và TSN.

Cần thêm thư mục vào PYTHONPATH hoặc append vào sys.path trước khi chạy backend:

import sys
sys.path.append(r"tsm/temporal-shift-module")
from ops.temporal_shift import TemporalShift
from ops.models import TSN

# 2️⃣ Frontend

Node.js & npm:

Node.js v22.20.0

npm 11.6.2

Production dependencies (package.json):

react 19.2.0

react-dom 19.2.0

Dev dependencies (package.json):

@types/node 22.14.0

@vitejs/plugin-react 5.0.0

typescript 5.8.2

vite 6.2.0

Tham khảo chi tiết trong frontend/package.json nếu cần rebuild hoặc chạy local frontend.

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

## VI. Danh sách sinh viên
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
