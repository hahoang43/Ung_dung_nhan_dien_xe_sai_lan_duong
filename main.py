import cv2
import os
from src.detector import VehicleDetector
from src.lane_monitor import LaneMonitor

# --- CẤU HÌNH ---
VIDEO_PATH = 'data/xe.mp4' # Đường dẫn video đầu vào (bạn cần thay đổi)
OUTPUT_PATH = 'output/result.mp4'

# Định nghĩa vùng làn đường (Polygon: danh sách các điểm x, y)
# LƯU Ý: Bạn cần chạy video một lần, print tọa độ chuột để lấy các điểm chính xác cho video của bạn.
# Đây là tọa độ giả lập.
LANES_CONFIG = [
    {
        "name": "Lan Xe May",
        "polygon": [(100, 400), (300, 400), (400, 700), (0, 700)], # Hình thang bên trái
        "allowed_classes": [3], # 3: Motorcycle
        "color": (0, 255, 0) # Xanh lá
    },
    {
        "name": "Lan O To",
        "polygon": [(305, 400), (600, 400), (900, 700), (405, 700)], # Hình thang bên phải
        "allowed_classes": [2, 5, 7], # 2: Car, 5: Bus, 7: Truck
        "color": (255, 0, 0) # Xanh dương
    }
]

def main():
    # 1. Khởi tạo
    if not os.path.exists('output'):
        os.makedirs('output')
        
    detector = VehicleDetector() # Tự động tải yolov8n.pt
    monitor = LaneMonitor(LANES_CONFIG)

    # 2. Mở video
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print(f"Không thể mở video: {VIDEO_PATH}")
        print("Đang sử dụng Webcam (0) để thay thế...")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Không thể mở Webcam.")
            return

    # Lấy thông số video để lưu output
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # Video Writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (width, height))

    print("Bắt đầu xử lý... Nhấn 'q' để thoát.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 3. Phát hiện xe
        detections = detector.detect(frame)

        # 4. Kiểm tra làn đường và vẽ kết quả
        processed_frame, violations = monitor.check_violations(detections, frame)

        # 5. Hiển thị và lưu
        cv2.imshow('Wrong Lane Detection', processed_frame)
        out.write(processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Hoàn thành! Video đã lưu tại {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
