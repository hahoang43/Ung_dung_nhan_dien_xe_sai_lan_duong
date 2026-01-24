Hệ Thống Nhận Diện Xe Sai Làn Đường (AI Traffic Violation Detection)
Dự án sử dụng Python, OpenCV và YOLOv8 (Ultralytics) để phát hiện phương tiện giao thông, theo dõi quỹ đạo (Tracking) và đếm số lượng xe đi vào làn đường cấm theo thời gian thực.

Hệ thống được tối ưu hóa cho GPU NVIDIA (RTX 3050 trở lên) để đạt hiệu suất cao nhất.

🚀 Tính Năng Nổi Bật
Vẽ làn đường tương tác: Không cần sửa code tọa độ thủ công. Khi chạy chương trình, bạn có thể dùng chuột click trực tiếp lên video để vẽ vùng làn đường.

Nhận diện đa phương tiện: Hỗ trợ phát hiện Ô tô, Xe máy, Xe buýt, Xe tải.

Tracking & Đếm xe: Sử dụng ID theo dõi để đếm chính xác số lượng xe vi phạm (không đếm trùng lặp).

Tối ưu hóa GPU: Cấu hình chạy mượt mà trên card đồ họa NVIDIA (khắc phục hiện tượng delay khung hình).

Giao diện trực quan: Hiển thị khung đỏ cảnh báo và bảng thống kê số lượng vi phạm ngay trên video.

📂 Cấu trúc thư mục
Plaintext

Nhandienxesailan/
│
├── data/                  # Chứa video đầu vào
│   └── xe.mp4             # Video mẫu
│
├── output/                # Chứa video kết quả (tự động tạo)
│
├── src/                   # Mã nguồn chính
│   ├── __init__.py
│   ├── detector.py        # (Tùy chọn) Class wrapper cho YOLO
│   ├── lane_monitor.py    # Class xử lý logic vi phạm và đếm xe
│   ├── lane_drawer.py     # Class hỗ trợ vẽ làn đường bằng chuột
│   └── utils.py           # Các hàm hỗ trợ hình học
│
├── main.py                # Chương trình chạy chính
└── requirements.txt       # Danh sách thư viện
🛠 Cài đặt
1. Yêu cầu hệ thống
Python 3.8 trở lên.

Khuyên dùng: Máy tính có GPU NVIDIA (Để chạy thời gian thực). Nếu dùng CPU sẽ chậm hơn.

2. Cài đặt thư viện
Bước 1: Tạo môi trường ảo (Khuyến khích)

Bash

python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
Bước 2: Cài đặt PyTorch hỗ trợ GPU (QUAN TRỌNG) Lưu ý: Cần cài đặt PyTorch phiên bản CUDA trước các thư viện khác để tránh lỗi xung đột hoặc tràn bộ nhớ.

Chạy lệnh sau (dành cho Windows + Card NVIDIA):

Bash

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 --no-cache-dir
Bước 3: Cài đặt các thư viện còn lại

Bash

pip install ultralytics opencv-python numpy
📖 Hướng dẫn sử dụng
Bước 1: Chuẩn bị Video
Copy video giao thông cần xử lý vào thư mục data/ và đổi tên file trong main.py (biến VIDEO_PATH) nếu cần.

Bước 2: Chạy chương trình
Mở terminal tại thư mục gốc dự án và chạy:

Bash

python main.py
Bước 3: Cấu hình Làn đường (Vẽ tay)
Khi chương trình bắt đầu, frame đầu tiên của video sẽ hiện lên. Hãy nhìn hướng dẫn trên màn hình:

Vẽ làn Xe Máy: Click chuột trái vào 4 góc để bao quanh làn xe máy -> Nhấn phím n để xác nhận.

Vẽ làn Ô Tô: Click chuột trái vào 4 góc bao quanh làn ô tô -> Nhấn phím n để xác nhận.

Sau khi vẽ xong, video sẽ tự động chạy và bắt đầu nhận diện.

Bước 4: Xem kết quả
Hệ thống sẽ hiển thị video với các khung nhận diện.

Khung Đỏ: Xe đi sai làn (kèm cảnh báo).

Thống kê số lượng xe vi phạm sẽ hiện ở góc trái màn hình.

Video kết quả được lưu tự động tại output/result.mp4.

⚙️ Tùy chỉnh (Trong file main.py)
VIDEO_PATH: Đường dẫn file video đầu vào.

MODEL_PATH:

Dùng yolov8m.pt (Medium) cho cân bằng giữa Tốc độ và Chính xác (Khuyên dùng cho RTX 3050).

Dùng yolov8n.pt (Nano) nếu máy cấu hình yếu.

Dùng yolov8l.pt (Large) nếu cần độ chính xác cực cao và máy mạnh.

IMAGE_SIZE: Mặc định 640. Có thể tăng lên 1280 nếu muốn nhận diện xe ở rất xa (nhưng sẽ nặng máy hơn).

❓ Khắc phục lỗi thường gặp
Lỗi MemoryError khi cài PyTorch:

Hãy chắc chắn bạn đã thêm cờ --no-cache-dir vào lệnh pip install.

Chương trình báo "Running on CPU" dù có card rời:

Bạn đã cài nhầm bản PyTorch CPU. Hãy gỡ ra (pip uninstall torch torchvision) và cài lại theo hướng dẫn ở Bước 2 phần Cài đặt.

Khung nhận diện bị lệch so với xe (Delay):

Do máy xử lý không kịp. Hãy giảm IMAGE_SIZE xuống 640 hoặc dùng model nhẹ hơn (yolov8n.pt).