# Hệ Thống Nhận Diện Xe Sai Làn Đường
## AI Traffic Violation Detection System

Ứng dụng thông minh phát hiện và đếm số lượng phương tiện giao thông vi phạm luật sử dụng làn đường theo thời gian thực, sử dụng công nghệ nhận diện ảnh AI (YOLOv8) và theo dõi quỹ đạo (Vehicle Tracking).

## 🎬 Video Demo
📽️ **[Xem Video Demo tại đây](https://drive.google.com/file/d/1y6BpkX6QqqB3Nd-eQxkzXYM8mpwRTmlM/view?usp=sharing)** - Nhom9 Ứng dụng Nhận Diện Xe Sai Làn Đường

###  Mục đích
- **Giám sát giao thông**: Phát hiện xe vi phạm làn đường (xe máy chạy làn ô tô, ô tô chạy làn xe máy, v.v.)
- **Thống kê tự động**: Đếm chính xác số lượng xe sai làn mà không bị trùng lặp
- **Phân tích dữ liệu**: Hỗ trợ quản lý giao thông và lập kế hoạch an toàn đường
- **Hỗ trợ thực thi pháp luật**: Cung cấp bằng chứng hình ảnh cho các lực lượng chức năng

Hệ thống được **tối ưu hóa cho GPU NVIDIA** (RTX 3050 trở lên) để đạt tốc độ xử lý thời gian thực.

## Tính Năng Nổi Bật

**Vẽ làn đường tương tác**
   - Không cần sửa code tọa độ thủ công
   - Click chuột trực tiếp lên video để vẽ vùng làn đường
   - Hỗ trợ Undo (nhấn chuột phải) và Reset (phím 'r')

**Nhận diện đa phương tiện**
   - Ô tô, Xe máy, Xe buýt, Xe tải

**Tracking & Đếm chính xác**
   - Mỗi xe được gán ID duy nhất qua các khung hình
   - Lưu lũy tích ID xe sai làn (dùng Set → không đếm trùng)
   - Hiển thị thống kê theo từng làn đường

**Tối ưu hóa GPU**
   - Chạy mượt mà trên card NVIDIA
   - Hỗ trợ CPU nếu không có GPU (chậm hơn)

**Giao diện trực quan**
   - Khung đỏ cảnh báo cho xe sai làn
   - Text hiển thị ID xe vi phạm
   - Bảng thống kê tổng số vi phạm theo làn

##  Cài đặt

### Yêu cầu hệ thống

- **Python**: 3.8 trở lên
- **GPU** (Khuyến khích): NVIDIA RTX 3050 hoặc cao hơn
  - Nếu không có GPU, chương trình vẫn chạy trên CPU nhưng chậm hơn
- **RAM**: Tối thiểu 4GB (khuyến khích 8GB+)
- **Disk**: Ít nhất 2GB cho model YOLO

### 2️ Cài đặt từng bước

#### Bước 1: Tạo môi trường ảo (Khuyến khích)

```bash
python -m venv .venv

# Windows:
.\.venv\Scripts\activate

# Linux/Mac:
source .venv/bin/activate
```

#### Bước 2: Cài PyTorch hỗ trợ GPU ( QUAN TRỌNG)

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
- Nếu in `True` → GPU hoạt động 
- Nếu in `False` → Sử dụng CPU 
##  Hướng dẫn sử dụng

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

####  Vẽ Làn Xe Máy (Làn 1):

1. **Click chuột trái** 4 lần vào 4 góc của làn xe máy
   - Để tạo đa giác (polygon) bao quanh làn
   - Điểm sẽ hiển thị khi click
2. **Nhấn phím 'n'** để hoàn thành
3. **Nhấn phím 'r'** nếu muốn vẽ lại

#### Vẽ Làn Ô Tô (Làn 2):

Làm tương tự như trên cho làn ô tô.

> **💡 Mẹo**: Click chuột phải để undo điểm vừa click (xóa điểm cuối cùng)

### Bước 4: Chương trình tự động chạy

Sau khi vẽ xong 2 làn, video sẽ bắt đầu phát:

- **Khung đỏ**: Xe vi phạm (sai làn)
- **Bảng thống kê**: Góc trái màn hình hiển thị tổng số xe sai làn
- **Thoát**: Nhấn phím 'q'

### Bước 5: Xem kết quả

Video xử lý tự động lưu vào: **`output/result.mp4`**

##  Hỗ trợ & Báo cáo lỗi

Nếu gặp vấn đề:
1. Kiểm tra lại cài đặt PyTorch
2. Chắc chắn GPU được nhận diện (`torch.cuda.is_available()`)
3. Thử dùng model nhẹ hơn (`yolov8n.pt`)
4. Kiểm tra file video hợp lệ (codec, format)
