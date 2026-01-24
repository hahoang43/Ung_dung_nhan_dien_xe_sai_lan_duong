import cv2
import os
import torch
from src.lane_monitor import LaneMonitor
from src.lane_drawer import LaneDrawer
from ultralytics import YOLO

# --- CẤU HÌNH ---
VIDEO_PATH = 'data/xe.mp4' 
OUTPUT_PATH = 'output/result.mp4'

# Cấu hình tối ưu cho RTX 3050 (Vừa nhanh vừa chính xác)
MODEL_PATH = 'yolov8m.pt' 
IMAGE_SIZE = 640 

LANES_TEMPLATE = [
    {
        "name": "Lan Xe May",
        "polygon": [], 
        "allowed_classes": [3], # 3: Motorcycle
        "color": (0, 255, 0) 
    },
    {
        "name": "Lan O To",
        "polygon": [],
        "allowed_classes": [2, 5, 7], # 2: Car, 5: Bus, 7: Truck
        "color": (255, 0, 0) 
    }
]

def main():
    # 1. Kiểm tra phần cứng
    device = '0' if torch.cuda.is_available() else 'cpu'
    print(f"--- ĐANG CHẠY TRÊN: {torch.cuda.get_device_name(0) if device == '0' else 'CPU'} ---")
    
    if not os.path.exists('output'):
        os.makedirs('output')

    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("Lỗi: Không thể mở video.")
        return

    # 2. Vẽ làn đường (Chỉ làm 1 lần lúc đầu)
    ret, first_frame = cap.read()
    if not ret: return
    
    print("\n--- CẤU HÌNH LÀN ĐƯỜNG (CỐ ĐỊNH) ---")
    drawer = LaneDrawer()
    final_lanes_config = []
    
    for lane_cfg in LANES_TEMPLATE:
        # Hàm này sẽ mở cửa sổ để bạn click chuột vẽ
        points = drawer.get_lane_polygon(first_frame, lane_cfg["name"])
        lane_cfg["polygon"] = points
        final_lanes_config.append(lane_cfg)
        
    drawer.close()
    
    # 3. Khởi tạo AI & Monitor
    print(f"Đang tải model {MODEL_PATH}...")
    model = YOLO(MODEL_PATH)
    
    # Khởi tạo bộ giám sát với tọa độ tĩnh vừa vẽ
    monitor = LaneMonitor(final_lanes_config)

    # 4. Bắt đầu xử lý video
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # Tua về đầu
    
    # Cấu hình lưu video
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(OUTPUT_PATH, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    print("Bắt đầu chạy... (Nhấn 'q' để thoát)")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # --- TRACKING (Bám theo xe để lấy ID đếm số lượng) ---
        # persist=True: Giữ ID xe ổn định qua các khung hình
        results = model.track(
            frame, 
            persist=True, 
            verbose=False, 
            imgsz=IMAGE_SIZE, 
            conf=0.5, 
            device=device,
            classes=[2, 3, 5, 7] # Chỉ nhận diện xe, bỏ qua người/vật khác
        )[0]

        detections = []
        # Kiểm tra xem có xe nào không
        if results.boxes is not None and results.boxes.id is not None:
            # Lấy dữ liệu từ GPU về CPU
            boxes = results.boxes
            xyxys = boxes.xyxy.cpu().numpy()
            ids = boxes.id.cpu().numpy()
            clss = boxes.cls.cpu().numpy()
            confs = boxes.conf.cpu().numpy()

            # Đóng gói dữ liệu gửi sang LaneMonitor
            for xyxy, track_id, cls_id, conf in zip(xyxys, ids, clss, confs):
                x1, y1, x2, y2 = map(int, xyxy)
                detections.append((x1, y1, x2, y2, int(track_id), conf, int(cls_id)))

        # --- KIỂM TRA LÀN & ĐẾM XE ---
        processed_frame, violation_ids = monitor.check_violations(detections, frame)

        # Hiển thị thông tin phần cứng
        cv2.putText(processed_frame, f"Mode: FIXED | GPU: ON", (10, height - 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow('Phat hien sai lan (Co dinh)', processed_frame)
        out.write(processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Hoàn thành!")

if __name__ == "__main__":
    main()