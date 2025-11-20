## 📘 Mục lục
[I. Giới thiệu & Cấu hình đề xuất]
[II. Cách chạy Local]
[III. Cách chạy với Docker]
[IV. Các lỗi thường gặp]

I. Giới thiệu & Cấu hình đề xuất
Em chào thầy ạ
Đây là phần hướng dẫn chạy project ạ

# Note: Model (ResNet50 + TSM) sẽ mặc định dùng GPU để xử lí
# Laptop của em: Gigabyte G5
# Operating system: Window
# RAM: 8GB
# GPU: NVIDIA GeForce RTX 3050 Laptop
# CPU: 12th Gen Intel(R) Core(TM) i5-12500H (2.50 GHz)

# Để có thể chạy dự đoán bạo lực realtime, nên đảm bảo cấu hình tầm này ạ

III. Chạy local - Có video hướng dẫn
1. Chạy backend
Step 1: cd tới backend folder
Step 2: Nhập "python -m uvicorn main.server:app --reload"

Dấu hiệu khi backend chạy dc:
- Model được load
- Có thông báo server chạy dc và địa chỉ của server
- Terminal hỏi số lượng camera

2. Chạy frontend
Step 1: cd tới frontend
Step 2: npm install (để có thư mục node_modules)
Step 2: Nhập "npx vite --host --port 5731"

Dấu hiệu khi frontend chạy dc: Có link hiện ra

3. Kết nối camera:

- Bọn em thường dùng app IP webcam ở Google play

- Khi nhấn start server thì nó sẽ hiện ra cái ip của camera, trông như thế này: http://192.168.1.60:8080 (Thầy có thể bấm vô link để điều chỉnh camera)
- Mỗi lần bật là app đổi ip nên khúc connect cam vẫn phải thủ công một chút
- Yêu cầu là laptop + điện thoại cùng wifi ạ

- Tuy nhiên, khi copy link camera vào backend và frontend, phải thêm "/video" vào nữa
http://192.168.1.14:8080 => http://192.168.1.14:8080/video 

Terminal hiển thị ra json, frontend render dc là chạy dc rồi ạ
Xin hãy xem video để minh họa trực quan hơn ạ

IV. Chạy với docker
# Link repo ở dockerhub
https://hub.docker.com/repository/docker/minhvanhanu/ati-docker-files/general

1. Chạy backend
- cd backend

- Build images: docker build -t vio-backend . 
# File docker nặng 12GB, nên nếu thầy ko muốn build images khi phải chờ lâu, có thể trực tiếp pull từ dockerhub của em
- Pull docker: docker pull minhvanhanu/ati-docker-files:backend

- Chạy backend: docker run -p 8000:8000 vio-backend

- Test backend:
docker exec -it <container_id> python -c "import torch; print(torch.__version__, torch.cuda.is_available())" 
# Kiểm tra torch version
2.1.0 True 
# Output ra như vậy là dc ạ

# Nếu dùng NVIDIA docker
docker run --gpus all -p 8000:8000 vio-backend 

2. Chạy frontend
- cd frontend

# nếu thầy muốn tự build images
- docker build -t vio-frontend . 

# nếu thầy muốn pull frontend của em về
- docker pull minhvanhanu/ati-docker-files:frontend 

- Chạy frontend: docker run -p 5731:80 vio-frontend

# Khi frontend hiện link http://localhost:5731 là OK
- Sau đó, kết nối camera như trong video hướng dẫn

V. Các lỗi thường gặp
- Các thư viện cần thiết: Xin thầy hãy check trong backend/requirements.txt và frontend/package.json
1. Port bị chiếm dụng => Kill bằng Pid
netstat -ano | findstr "TEN_PORT"
taskkill /PID <PID_NUMBER> /F

2. Không gửi hoặc nhận được dữ liệu qua API (Không thể sử dụng tính năng realtime hoặc offline analysis)
- File frontend cần check: 
# frontend/App.tsx (kiểm tra dòng fetch API "/realtime") 
# frontend/components/VideoUploader.tsx (kiểm tra dòng fetch API "/upload")

- File backend cần check: main/server.py -- chạy thử
# Check link server và link frontend
# Có thể server là http:127:...
# Nhưng có thể frontend khi fetch lại không dùng địa chỉ của server

- Đảm bảo frontend đang gọi đúng endpoint

# Thầy hãy thử nhập {link server + "/docs"} vào trình duyệt để thử API, xem server có chạy không
# Nếu server chạy mà frontend không gen giao diện => Sai API

3. Realtime quá chậm đến mức có thể coi là mất realtime
- Vấn đề với __pycache__: Lúc mới chạy, chương trình có thể chưa tạo ra các tệp .pyc trong thư mục __pycache__, khiến chương trình chạy chậm.
- Giải pháp: Hãy để cho hệ thống chạy và sau khoảng 40 JSON (hoặc nhiều hơn) được tạo ra, chương trình sẽ chạy nhanh dần và đạt hiệu suất realtime ổn định.

4. Server không chạy được
- Thường là do 1 trong 2 lỗi sau:
# Input type mismatch: Num of camera yêu cầu int, nhưng nhập giá trị khác (String...)
# Link camera không đúng: Khi backend không tìm thấy địa chỉ camera => Không có frame truyền vào server => cv2 found no frame

- Xin thầy đảm bảo link camera đúng (có /video). 
- Với frontend, thầy có thể không nhập hoặc nhập sai
- Nhưng với backend, mọi thứ phải đúng

- Nguyên nhân lỗi: Backend và Frontend kết nối camera độc lập
# Frontend có nhiệm vụ stream, hiển thị FPS cao nhất có thể
# Tuy nhiên, backend mỗi giây chỉ lấy một vài frame

- Em không muốn project bị chồng chéo logic, nên bọn em quyết định thiết kế theo hướng đó

- Cách sửa: Chạy lại server và frontend từ đầu

6. Frontend không khởi chạy
- Terminal yêu cầu tải vite@7.2.4
- Lí do: Chưa có node_modules
- Solution: cd frontend => Tải dependencies với lệnh: npm install

Nếu có vấn đề gì, xin hãy liên hệ với em
# Email: hoangvanminh2100@gmail.com
# Phone number + zalo: 0399593750
# Student ID để liên lạc qua team, qua outlook: 2301040117
# Messenger, facebook: https://www.facebook.com/minh.van.48176/