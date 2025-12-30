# Hệ Thống Nhận Diện Xe Sai Làn Đường

Dự án sử dụng Python, OpenCV và YOLOv8 để phát hiện các phương tiện giao thông và cảnh báo khi chúng đi vào làn đường không được phép.

## Cấu trúc thư mục

```
Nhandienxesailan/
│
├── data/               # Chứa video đầu vào (bạn cần thêm video vào đây)
├── output/             # Chứa video kết quả sau khi xử lý
├── models/             # Chứa file weights của model (tự động tải yolov8n.pt)
├── src/                # Mã nguồn chính
│   ├── __init__.py
│   ├── detector.py     # Class xử lý phát hiện xe bằng YOLO
│   ├── lane_monitor.py # Class xử lý logic làn đường và vi phạm
│   └── utils.py        # Các hàm hỗ trợ vẽ và hình học
├── main.py             # File chạy chính
└── requirements.txt    # Các thư viện cần thiết
```

## Cài đặt

1.  **Cài đặt Python:** Đảm bảo bạn đã cài đặt Python (khuyên dùng 3.8 trở lên).
2.  **Cài đặt thư viện:**
    Mở terminal tại thư mục dự án và chạy:
    ```bash
    pip install -r requirements.txt
    ```
    (Lệnh này sẽ cài đặt `opencv-python`, `numpy`, và `ultralytics`).

## Hướng dẫn sử dụng

1.  **Chuẩn bị Video:**
    *   Copy video giao thông bạn muốn kiểm tra vào thư mục `data/`.
    *   Đổi tên thành `sample_video.mp4` hoặc sửa đường dẫn `VIDEO_PATH` trong file `main.py`.

2.  **Cấu hình Làn đường (Quan trọng):**
    *   Mỗi camera/video có góc quay khác nhau, nên tọa độ các làn đường sẽ khác nhau.
    *   Mở file `main.py`.
    *   Tìm biến `LANES_CONFIG`.
    *   Bạn cần điều chỉnh các tọa độ `polygon` `[(x1, y1), (x2, y2), ...]` sao cho khớp với vạch kẻ đường trong video của bạn.
    *   *Mẹo:* Bạn có thể viết một đoạn script nhỏ dùng `cv2.setMouseCallback` để click lên ảnh và lấy tọa độ chính xác.

3.  **Chạy chương trình:**
    ```bash
    python main.py
    ```

4.  **Kết quả:**
    *   Cửa sổ video sẽ hiện lên với các khung bao quanh xe.
    *   Xe đi đúng làn sẽ có chữ "DUNG LAN" (màu xanh).
    *   Xe đi sai làn sẽ có chữ "SAI LAN" (màu đỏ) và khung đỏ.
    *   Video kết quả được lưu tại `output/result.mp4`.

## Công nghệ sử dụng

*   **YOLOv8 (Ultralytics):** Để nhận diện phương tiện (Ô tô, xe máy, xe buýt, xe tải).
*   **OpenCV:** Xử lý ảnh, vẽ đồ họa và tính toán hình học (điểm nằm trong đa giác).
