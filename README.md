# 🚗 Hệ Thống Nhận Diện Xe Sai Làn Đường
## AI Traffic Violation Detection System

Ứng dụng thông minh phát hiện và đếm số lượng phương tiện giao thông vi phạm luật sử dụng làn đường theo thời gian thực, sử dụng công nghệ nhận diện ảnh AI (YOLOv8) và theo dõi quỹ đạo (Vehicle Tracking).

## 🎬 Video Demo
![Nhom9 Demo - Ứng dụng Nhận Diện Xe Sai Làn Đường](Nhom9-DemoUngDungNhanDienXeSaiLanDuong.mp4)

### 📌 Mục đích
- **Giám sát giao thông**: Phát hiện xe vi phạm làn đường (xe máy chạy làn ô tô, ô tô chạy làn xe máy, v.v.)
- **Thống kê tự động**: Đếm chính xác số lượng xe sai làn mà không bị trùng lặp
- **Phân tích dữ liệu**: Hỗ trợ quản lý giao thông và lập kế hoạch an toàn đường
- **Hỗ trợ thực thi pháp luật**: Cung cấp bằng chứng hình ảnh cho các lực lượng chức năng

Hệ thống được **tối ưu hóa cho GPU NVIDIA** (RTX 3050 trở lên) để đạt tốc độ xử lý thời gian thực.

## ✨ Tính Năng Nổi Bật

✅ **Vẽ làn đường tương tác**
   - Không cần sửa code tọa độ thủ công
   - Click chuột trực tiếp lên video để vẽ vùng làn đường
   - Hỗ trợ Undo (nhấn chuột phải) và Reset (phím 'r')

✅ **Nhận diện đa phương tiện**
   - Ô tô, Xe máy, Xe buýt, Xe tải

✅ **Tracking & Đếm chính xác**
   - Mỗi xe được gán ID duy nhất qua các khung hình
   - Lưu lũy tích ID xe sai làn (dùng Set → không đếm trùng)
   - Hiển thị thống kê theo từng làn đường

✅ **Tối ưu hóa GPU**
   - Chạy mượt mà trên card NVIDIA
   - Hỗ trợ CPU nếu không có GPU (chậm hơn)

✅ **Giao diện trực quan**
   - Khung đỏ cảnh báo cho xe sai làn
   - Text hiển thị ID xe vi phạm
   - Bảng thống kê tổng số vi phạm theo làn

## 📂 Cấu trúc thư mục

```
Ung_dung_nhan_dien_xe_sai_lan_duong/
│
├── data/                  # 📁 Chứa video đầu vào
│   └── xe.mp4             # Video mẫu để test
│
├── output/                # 📁 Chứa video kết quả (tự động tạo)
│   └── result.mp4         # Video đầu ra sau xử lý
│
├── src/                   # 📁 Mã nguồn chính
│   ├── __init__.py
│   ├── detector.py        # (Tùy chọn) Class wrapper YOLO nhận diện xe
│   ├── lane_monitor.py    # ⭐ Class xử lý logic vi phạm & đếm xe
│   ├── lane_drawer.py     # ⭐ Class vẽ làn đường bằng chuột
│   ├── utils.py           # Hàm hỗ trợ hình học (kiểm tra điểm trong polygon)
│   └── __pycache__/       # Cache Python (tự động tạo)
│
├── main.py                # ⭐ Chương trình chạy chính (entry point)
├── requirements.txt       # Danh sách thư viện cần cài
├── yolov8m.pt             # Model YOLO v8 Medium (download lần đầu)
└── README.md              # Tài liệu này
```

**⭐ = File quan trọng**
## 🛠 Cài đặt

### 1️⃣ Yêu cầu hệ thống

- **Python**: 3.8 trở lên
- **GPU** (Khuyến khích): NVIDIA RTX 3050 hoặc cao hơn
  - Nếu không có GPU, chương trình vẫn chạy trên CPU nhưng chậm hơn
- **RAM**: Tối thiểu 4GB (khuyến khích 8GB+)
- **Disk**: Ít nhất 2GB cho model YOLO

### 2️⃣ Cài đặt từng bước

#### Bước 1: Tạo môi trường ảo (Khuyến khích)

```bash
python -m venv .venv

# Windows:
.\.venv\Scripts\activate

# Linux/Mac:
source .venv/bin/activate
```

#### Bước 2: Cài PyTorch hỗ trợ GPU (⚠️ QUAN TRỌNG)

> **Lưu ý**: Cài PyTorch CUDA trước các thư viện khác để tránh xung đột hoặc lỗi bộ nhớ.

**Cho Windows + Card NVIDIA:**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 --no-cache-dir
```

**Cho máy không có GPU (CPU):**
```bash
pip install torch torchvision torchaudio
```

#### Bước 3: Cài thư viện còn lại

```bash
pip install -r requirements.txt
```

Hoặc cài thủ công:
```bash
pip install ultralytics opencv-python numpy
```

**Xác nhận cài đặt thành công:**
```bash
python -c "import torch; print(torch.cuda.is_available())"
```
- Nếu in `True` → GPU hoạt động ✅
- Nếu in `False` → Sử dụng CPU ⚠️
## 📖 Hướng dẫn sử dụng

### Bước 1: Chuẩn bị video đầu vào

1. Copy file video giao thông vào thư mục `data/`
2. Sửa tên file trong `main.py` (nếu cần):
   ```python
   VIDEO_PATH = 'data/xe.mp4'  # ← Đổi đây nếu khác tên
   ```

### Bước 2: Chạy chương trình

```bash
python main.py
```

### Bước 3: Vẽ làn đường (Tương tác bằng chuột)

Khi chạy, frame đầu tiên của video sẽ hiện lên. Bạn cần vẽ 2 làn đường:

#### 🟢 Vẽ Làn Xe Máy (Làn 1):

1. **Click chuột trái** 4 lần vào 4 góc của làn xe máy
   - Để tạo đa giác (polygon) bao quanh làn
   - Điểm sẽ hiển thị khi click
2. **Nhấn phím 'n'** để hoàn thành
3. **Nhấn phím 'r'** nếu muốn vẽ lại

#### 🔴 Vẽ Làn Ô Tô (Làn 2):

Làm tương tự như trên cho làn ô tô.

> **💡 Mẹo**: Click chuột phải để undo điểm vừa click (xóa điểm cuối cùng)

### Bước 4: Chương trình tự động chạy

Sau khi vẽ xong 2 làn, video sẽ bắt đầu phát:

- 🟥 **Khung đỏ**: Xe vi phạm (sai làn)
- 📊 **Bảng thống kê**: Góc trái màn hình hiển thị tổng số xe sai làn
- ⏹️ **Thoát**: Nhấn phím 'q'

### Bước 5: Xem kết quả

Video xử lý tự động lưu vào: **`output/result.mp4`**

## ⚙️ Tùy chỉnh cấu hình

Mở file `main.py` và sửa các biến sau:

### 🎬 Video & Output

```python
VIDEO_PATH = 'data/xe.mp4'        # Đường dẫn video đầu vào
OUTPUT_PATH = 'output/result.mp4' # Đường dẫn video đầu ra
```

### 🤖 Model YOLO

```python
MODEL_PATH = 'yolov8m.pt'  # Model để dùng

# Lựa chọn:
# - yolov8n.pt  (Nano):  Nhanh nhất, độ chính xác thấp → Máy yếu
# - yolov8m.pt  (Medium): Cân bằng (KHUYÊN DÙNG) → RTX 3050
# - yolov8l.pt  (Large):  Chính xác cao, chậm hơn → Máy mạnh
# - yolov8x.pt  (Xlarge): Chính xác cực cao, rất chậm → GPU cao cấp
```

### 📸 Độ phân giải nhận diện

```python
IMAGE_SIZE = 640  # Mặc định 640x640 pixels

# Tăng lên 1280 nếu:
#   - Cần nhận diện xe ở rất xa
#   - Máy đủ mạnh
# (Lưu ý: Tăng → chậm hơn, tiêu tốn RAM hơn)
```

### 🚗 Loại xe cần phát hiện

```python
classes=[2, 3, 5, 7]  # Trong main.py, hàng ~88
# 2: Car (Ô tô)
# 3: Motorcycle (Xe máy)
# 5: Bus (Xe buýt)
# 7: Truck (Xe tải)
```

### 📐 Cấu hình làn đường

```python
LANES_TEMPLATE = [
    {
        "name": "Lan Xe May",
        "allowed_classes": [3],      # Chỉ xe máy được phép
        "color": (0, 255, 0)         # Màu hiển thị (BGR)
    },
    {
        "name": "Lan O To",
        "allowed_classes": [2, 5, 7], # Ô tô, buýt, tải được phép
        "color": (255, 0, 0)          # Màu hiển thị
    }
]
```

## ❓ Khắc phục lỗi thường gặp

### ❌ Lỗi: "MemoryError" khi cài PyTorch

**Nguyên nhân**: pip cache bộ nhớ quá lớn

**Cách sửa**:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 --no-cache-dir
```
⚠️ **Quan trọng**: Thêm cờ `--no-cache-dir`

---

### ❌ Lỗi: "Running on CPU" dù có card đồ họa

**Nguyên nhân**: Cài nhầm bản PyTorch CPU

**Cách sửa**:
```bash
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 --no-cache-dir
```

**Kiểm tra**:
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

---

### ❌ Lỗi: Video hiển thị chậm, khung hình lệch với xe

**Nguyên nhân**: Máy xử lý không kịp

**Cách sửa**:
1. **Giảm độ phân giải**: `IMAGE_SIZE = 640` (hoặc nhỏ hơn)
2. **Dùng model nhẹ hơn**: `MODEL_PATH = 'yolov8n.pt'`
3. **Tắt các chương trình khác** để giải phóng RAM/GPU

---

### ❌ Lỗi: "Không thể mở video"

**Nguyên nhân**: Đường dẫn video sai

**Cách sửa**:
1. Kiểm tra file tồn tại: `data/xe.mp4`
2. Sửa `VIDEO_PATH` trong `main.py`:
   ```python
   VIDEO_PATH = 'data/xe.mp4'  # Kiểm tra lại đường dẫn
   ```

---

### ❌ Lỗi: Module không tìm thấy (ImportError)

**Cách sửa**:
```bash
# Kích hoạt môi trường ảo trước
.\.venv\Scripts\activate  # Windows

# Sau đó cài lại thư viện
pip install -r requirements.txt
```

---

## 🔧 Hỗ trợ & Báo cáo lỗi

Nếu gặp vấn đề:
1. Kiểm tra lại cài đặt PyTorch
2. Chắc chắn GPU được nhận diện (`torch.cuda.is_available()`)
3. Thử dùng model nhẹ hơn (`yolov8n.pt`)
4. Kiểm tra file video hợp lệ (codec, format)